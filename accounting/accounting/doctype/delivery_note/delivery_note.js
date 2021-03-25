// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
	onload(frm) {
		frm.set_query("customer", function(){
			return {
				"filters": {
					"party_type": 'Customer'
				}
			}
		})
	},
	sales_order(frm){
		frappe.call({
			method: 'accounting.accounting.doctype.delivery_note.delivery_note.get_sales_order_items',
			args: {
				name: frm.doc.sales_order
			},
			callback: function(r) {
				var parent = r.message

				$.each(parent, function(index, row){
					var childDocType = frm.add_child("items")
					childDocType.item_name = row.item_name
					childDocType.item_rate = row.rate
					childDocType.item_quantity = row.item_quantity
					childDocType.amount = row.amount
					
					frm.refresh_fields()
				})
			}
		})
	},
	refresh(frm){
		if(frm.doc.docstatus) {
			frm.add_custom_button(__('Sales Invoice'), function(){
				if(frm.doc.docstatus){
					var doc_details = {
						customer: frm.doc.customer,
						delivery_note: frm.doc.name,
						total_amount: frm.doc.total_amount
					}
					frappe.new_doc('Sales Invoice', doc_details)
				}
			},__("Create"))
		}
	}
});

frappe.ui.form.on('Delivery Note Item', {
	item_name(frm){
		calculate_total(frm)
		frm.refresh()
	},
	item_rate(frm){
		calculate_total(frm)
		frm.refresh()
	},
	item_quantity(frm){
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
		quantity = quantity + items[i].item_quantity;
	}

	frm.set_value('total_amount', flt(total));
	frm.set_value('total_quantity', quantity);
}
