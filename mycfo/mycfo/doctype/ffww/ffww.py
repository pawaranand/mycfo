# -*- coding: utf-8 -*-
# Copyright (c) 2015, Indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
#from erpnext.utilities.address_and_contact import load_address_and_contact
import json

class FFWW(Document):
	def validate(self):
		self.validate_designation()
		self.validate_ffww()
		self.validate_dupicate_designation()

	def validate_designation(self):
		if not self.get('designation'):
			frappe.msgprint("At least one designation must be specified in designation child table",raise_exception=1)

	def validate_ffww(self):
		if frappe.db.sql("""select name from `tabFFWW` where customer='%s' and contact='%s' and  name!='%s'"""%(self.customer,self.contact,self.name)):
			name = frappe.db.sql("""select name from `tabFFWW` where customer='%s' and contact='%s' 
							and name!='%s'"""%(self.customer,self.contact,self.name),as_list=1)
			frappe.msgprint("customer %s already linked with contact %s in record %s"%(self.customer,self.contact,name[0][0]))

	def validate_dupicate_designation(self):
		designation_list = []
		if self.get('designation'):
			for d in self.get('designation'):
				if d.designation not in designation_list:
					designation_list.append(d.designation)
				else:
					frappe.msgprint("Duplicate designation name is not allowed",raise_exception=1)
					break

	def clear_child_table(self):
		self.set('more_contact_details', [])


@frappe.whitelist()
def make_address(source_name, target_doc=None):
	return _make_address(source_name, target_doc)

def _make_address(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		pass

	doclist = get_mapped_doc("FFWW", source_name,
		{"FFWW": {
			"doctype": "Address",
			"field_map": {
				"contact": "contact"
				# "company_name": "customer_name",
				# "contact_no": "phone_1",
				# "fax": "fax_1"
			}
		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	return doclist

@frappe.whitelist()
def make_contact(contact=None):
	contact_details = []
	contact_details = frappe.db.get_values('Contact Details',{'parent':contact},['contact_type','email_id','mobile_no','country_code','country'])
	if len(contact_details)>0:
		return contact_details
	else:
		return contact_details

def get_active_customers(doctype, txt, searchfield, start, page_len, filters):
	from frappe.desk.reportview import get_match_cond
	txt = "%{}%".format(txt)
	return frappe.db.sql("""select distinct customer
		from `tabProject Commercial`
		where docstatus < 2
		and customer is not null
			and project_status='Active'""")