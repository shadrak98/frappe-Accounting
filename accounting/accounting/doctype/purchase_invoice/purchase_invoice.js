// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	onload(frm){
		frm.set_query("supplier", function(){
			return {
				"filters": {
					"party_type": "Supplier"
				}
			}
		})
	},
	purchase_receipt(frm){
		frappe.call({
			method: 'accounting.accounting.doctype.purchase_invoice.purchase_invoice.get_purchase_receipt_items',
			args: {
				name: frm.doc.purchase_receipt
			},
			callback: function(r) {
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
		frm.refresh()
	}
});

frappe.ui.form.on('Purchase Invoice', {
	refresh(frm) {
		if(frm.doc.docstatus){
			frm.add_custom_button(__('Make Payment'), function(){
				frappe.new_doc('Payment Entry', {
					payment_type: 'Pay',
					amount_paid: frm.doc.total_amount,
					party: frm.doc.supplier,
					party_type: 'Supplier'
					// payment_reference: frm.doc.name
				})
			})
		}
	}
});

frappe.ui.form.on('Purchase Invoice Item',{
	item_name(frm){
		calculate_total(frm)
		frm.refresh_fields()
	},
	quantity(frm){
		calculate_total(frm)
		frm.refresh_fields()
	}
});

var calculate_total = function(frm){
	var total = 0;
	var quantity = 0;
	var items = frm.doc.items;

	for(var i in items) {
		items[i].amount = items[i].rate * items[i].quantity;
	}

	for(var i in items){
		total = total + items[i].amount;
		quantity = quantity + items[i].quantity;
	}
	frm.set_value('total_amount',total)
	frm.set_value('total_quantity',quantity)
}
