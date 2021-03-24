// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Receipt',{
	onload: function(frm){
		frm.set_query("supplier", function (){
			return {
				"filters": {
					"party_type": "Supplier"
				}
			}
		})
	},
	purchase_order(frm) {
		frappe.call({
			method: 'accounting.accounting.doctype.purchase_receipt.purchase_receipt.get_purchase_order_items',
			args: {
				name: frm.doc.purchase_order
			},
			callback: function(r){
				var parent = r.message

				$.each(parent, function(index, row){
					var childDocType = frm.add_child("items");
					childDocType.item_name = row.item_name;
					childDocType.quantity = row.item_quantity;
					childDocType.rate = row.item_rate;
					childDocType.amount = row.amount;
					calculate_total(frm)
					frm.refresh_fields()
				})
			}
		})
	}
});

frappe.ui.form.on('Purchase Receipt Item',{
	refresh: function(frm) {
		frm.add_custom_button(__('Purchase Invoice'), function(){
			if(frm.doc.docstatus) {
				var doc_details = {
					supplier : frm.doc.supplier,
					purchase_receipt : frm.doc.name
				}
				frappe.new_doc('Purchase Invoice', doc_details)
			}
		}, __("Create"));
	}
});

frappe.ui.form.on('Purchase Receipt Item', {
	item_name(frm){
		calculate_total(frm)
		self.refresh_fields()
	},
	quantity(frm){
		calculate_total(frm)
		self.refresh_fields()
	}
});

var calculate_total = function(frm) {
	var total = 0;
	var quantity = 0;
	var items = frm.doc.items;
	
	for (var d in items) {
		total = total + items[d].amount;
		quantity = quantity + items[d].item_quantity;
	}

	frm.set_value('total_amount', flt(total));
	frm.set_value('total_quantity', quantity);
}