// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
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
					var account_paid_from = doc.message['default_receivable_account'];
					var account_paid_to = doc.message['default_cash_account'];
					frm.set_value('account_paid_from', account_paid_from)
					frm.set_value('account_paid_to', account_paid_to)

				})
		}

		if(frm.doc.payment_reference) {
			var childDocType = frm.add_child("payment_reference");
			var invoice_type = '';
			if (frm.doc.payment_type == 'Receive') {
				invoice_type = 'Sales Invoice';
			} else {
				invoice_type = 'Purchase Invoice';
			}

			childDocType.reference_name = frm.doc.reference_name
			childDocType.reference_type = invoice_type

			frappe.db.get_value(invoice_type, frm.doc.reference, 'total_amount').then(amount => {
				childDocType.amount = amount.message.total_amount
				frm.doc.amount = amount.message.total_amount
				frm.refresh()
			})
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
});
