// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



{% include 'controllers/js/contact_address_common.js' %};

cur_frm.add_fetch('customer', 'customer_name', 'customer_name');


cur_frm.cscript.validate = function(doc, dt, dn) {
	calculate_all(doc, dt, dn);
}


var calculate_all = function(doc, dt, dn) {
	calculate_total_shares(doc, dt, dn);
	
}


var calculate_total_shares = function(doc, dt, dn) {
	var tbl = doc.shareholders_detail || [];

	var total_shares = 0;
	for(var i = 0; i < tbl.length; i++){
		total_shares += flt(tbl[i].equity_no );
	}
	doc.total = total_shares
	refresh_many(['total', 'shareholders_detail']);
}


cur_frm.fields_dict['shareholders_detail'].grid.get_field('shareholder_name').get_query = function(doc, cdt, cdn) {
	return {
		filters: {
			
			"contact_designation": 'Shareholder'
		}
	}
}


cur_frm.cscript.ebidta = function(doc,cdt,cdn){
	if(doc.annual_sales){
		if(doc.ebidta>doc.annual_sales){
			msgprint("EBIIDTA value must be less than annual sales")
			doc.ebidta=''
			refresh_field('ebidta');
		}
	}
}

cur_frm.cscript.pbt = function(doc,cdt,cdn){
	if(doc.annual_sales){
		if(doc.pbt>doc.annual_sales){
			msgprint("PBT value must be less than annual sales")
			doc.ebidta=''
			refresh_field('ebidta');
		}
	}
}

cur_frm.cscript.pat = function(doc,cdt,cdn){
	if(doc.annual_sales){
		if(doc.pbt>doc.annual_sales){
			msgprint("PAT value must be less than annual sales")
			doc.ebidta=''
			refresh_field('ebidta');
		}
	}
}