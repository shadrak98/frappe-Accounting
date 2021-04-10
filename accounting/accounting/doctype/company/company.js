// Copyright (c) 2021, shadrak and contributors
// For license information, please see license.txt

frappe.ui.form.on('Company', {
	setup(frm){
		frm.set_query("default_inventory_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("default_payable_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("default_receivable_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("default_cash_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("stock_received_but_not_billed", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("default_income_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
		frm.set_query("default_expense_account", function() {
			return {
				"filters": {
					"company": frm.doc.company_name,
					"is_group":0
				}
			}
		})
	}
});
