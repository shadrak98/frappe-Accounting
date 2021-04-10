// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	onload(frm) {
		var doctypes = ["Sales Invoice", "Purchase Invoice"];
		frm.set_query("document_type", function(){
			return {
				"filters": {
					"module": "Accounting",
					"name": [ "in", doctypes]
				}
			}
		})
	},
	setup(frm) {
		if(frm.doc.payment_type == 'Pay') {
			frm.doc.party_type = 'Supplier';

			frappe.db.get_value('Company', frm.doc.company, ['default_payable_account', 'default_cash_account'])
				.then(doc => {
					var account_paid_to = doc.message['default_payable_account'];
					var account_paid_from = doc.message['default_cash_account'];
					frm.set_value('account_paid_to', account_paid_to);
					frm.set_value('account_paid_from', account_paid_from);
				})
		}
		else {
			frm.doc.party_type = 'Customer';

			frappe.db.get_value('Company', frm.doc.company, ['default_receivable_account', 'default_cash_account'])
				.then(doc => {
					console.log("Customer-doc " + doc);
					var account_paid_from = doc.message['default_receivable_account'];
					var account_paid_to = doc.message['default_cash_account'];
					frm.set_value('account_paid_from', account_paid_from)
					frm.set_value('account_paid_to', account_paid_to)

				})
		}

		if(frm.doc.payment_reference) {
			var childDocType = frm.add_child("payment_reference");
			var invoice_type = '';
			var party = '';
			var party_type = '';
			if (frm.doc.payment_type == 'Receive') {
				invoice_type = 'Sales Invoice';
				party = frappe.db.get_value(invoice_type, frm.doc.document_name, "customer")
				party_type = "Customer";	
			} else {
				invoice_type = 'Purchase Invoice';
				party = frappe.db.get_value(invoice_type, frm.doc.document_name, "supplier")
				party_type = "Supplier";
			}

			childDocType.reference_name = frm.doc.reference_name
			childDocType.reference_type = invoice_type
			frm.doc.party_type = party_type
			frm.doc.party = party

			console.log(frm.doc.party + " " + frm.doc.party_type)

			frappe.db.get_value(invoice_type, frm.doc.reference, 'total_amount')
				.then(amount => {
					childDocType.amount = amount.message.total_amount
					frm.doc.amount = amount.message.total_amount
					frm.refresh_fields()
				})

			frm.refresh_fields()
		}
		frm.set_query("reference_type", "payment_reference", function() {
			if (frm.doc.party_type == "Supplier") {
				var doctypes = ["Purchase Invoice"];
			} else {
				var doctypes = ["Sales Invoice"]
			}
			return {
				filters: { "name": ["in", doctypes] }
			}
		})
	},

	// document_name(frm){
	// 	console.log(cur_frm + " " + frm.doc.document_name );
	// 	// var invoice = frm.doc.document_type == "Sales Invoice" ? frappe.get_doc("Sales Invoice", frm.doc.document_name) : frappe.get_doc("Purchase Invoice", frm.doc.document_name);
	// 	var invoice = frappe.get_doc("Sales Invoice", frm.doc.document_name);
	// 	var childDocType = cur_frm.add_child("payment_reference")

	// 	console.log(invoice.total_amount + " " + invoice)
	// 	childDocType.reference_type = frm.doc.document_type;
	// 	childDocType.reference_name = frm.doc.document_name;
	// 	childDocType.amount = invoice.total_amount;

	// 	console.log(frm + " " + childDocType.reference_name + " " + childDocType.amount)
	// 	refresh_fields("payment_reference");
	// }
});
