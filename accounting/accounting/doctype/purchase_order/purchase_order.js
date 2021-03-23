// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Order', 'onload', function(frm) {
	frm.set_query("supplier", function (){
		return {
			"filters": {
				"party_type": "Supplier"
			}
		}
	})
});

frappe.ui.form.on('Purchase Order Item', {
	item_name(frm, cdt, cdn) {
		//let row = frappe.get_doc(cdt, cdn);
		let row = locals[cdt][cdn];
		let qty = row.item_quantity;
		let rate = row.item_rate;
		let total = qty * rate;
		row.amount = total;
		// frm.refresh_field('amount');
		calculate_total(frm);
		frm.refresh_fields();
	},
	item_quantity(frm, cdt, cdn) {
		//let row = frappe.get_doc(cdt, cdn);
		let row = locals[cdt][cdn];
		let qty = row.item_quantity;
		let rate = row.item_rate;
		let total = qty * rate;
		row.amount = total;
		frm.refresh_field('amount');
		calculate_total(frm);
		frm.refresh_fields();
	}
});

var calculate_total = function(frm) {
	var total = 0;
	var quantity = 0;
	var items = frm.doc.item;
	for (var d in items) {
		total = total + items[d].amount;
		quantity = quantity + items[d].item_quantity;
	} 
	frm.set_value('total_amount', flt(total));
	frm.set_value('total_quantity', quantity);
}