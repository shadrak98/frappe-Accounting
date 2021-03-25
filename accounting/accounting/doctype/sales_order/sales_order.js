// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Order', {
	onload(frm){
		frm.set_query("customer", function(){
			return {
				"party_type": "Customer"
			}
		})
	},
	refresh(frm){
		if(frm.doc.docstatus){
			frm.add_custom_button(__('Delivery Note'), function(){
				if(frm.doc.docstatus){
					var doc_details = {
						customer: frm.doc.customer,
						sales_order: frm.doc.name,
						total_amount:frm.doc.total_amount
					}
					frappe.new_doc('Delivery Note', doc_details)
				}
			},__("Create"))
		}
	}
});

frappe.ui.form.on('Sales Order Item', {
	item_name(frm){
		calculate_total(frm)
		frm.refresh()
	},
	quantity(frm){
		calculate_total(frm)
		frm.refresh()
	}
})

var calculate_total = function(frm) {
	var total = 0;
	var quantity = 0;
	var items = frm.doc.items;

	for(var i in items) {
		total = total + items[i].amount;
		quantity = quantity + items[i].quantity;
	}

	frm.set_value('total_amount', flt(total));
	frm.set_value('total_quantity', quantity);
}