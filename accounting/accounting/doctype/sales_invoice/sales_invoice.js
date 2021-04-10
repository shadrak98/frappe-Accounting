// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	onload(frm) {
		frm.set_query("customer", function(){
			return {
				"filters": {
					"party_type": 'Customer'
				}
			}
		})
	},
	refresh(frm){
		if(frm.doc.docstatus){
			frm.add_custom_button(__('Make Payment'), function(){
				if(frm.doc.docstatus){
					// console.log(frm.doc.total_amount + " " + frm.doc.name)
					frappe.new_doc('Payment Entry', {
						payment_type:'Receive',
						amount: frm.doc.total_amount,
						party: frm.doc.customer,
						party_type: 'Customer'
					})
				}
			})
		}
	}
});

frappe.ui.form.on('Sales Invoice Item', {
	item_name(frm){
		calculate_total(frm)
		frm.refresh()
	},
	rate(frm){
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
		items[i].amount = items[i].quantity * items[i].rate;
	}

	for(var i in items) {
		total = total + items[i].amount;
		quantity = quantity + items[i].quantity;
	}

	frm.set_value('total_amount', flt(total));
	frm.set_value('total_quantity', quantity);
	console.log(total + " " + quantity);
}

