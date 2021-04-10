// Copyright (c) 2016, shadrak and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label":__("Company"),
			"fieldtype":"Link",
			"options":"Company",
			"default":frappe.defaults.get_user_default("Company"),
			"reqd":1
		},
		{
			"fieldname":"from_date",
			"label":__("From Date"),
			"fieldtype":"Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"reqd": 1,
			"width":"60px"
		},
		{
			"fieldname":"to_date",
			"label":__("To Date"),
			"fieldtype":"Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width":"60px"
		},
		{
			"fieldname":"account",
			"label":__("Account"),
			"fieldtype":"Link",
			"options":"Account",
			"get_query": function(){
				var company = frappe.query_report.get_filter_value('company');
				return {
					"doctype": "Account",
					"filters": {
						"company": company,
					}
				}
			}
		},
		{
			"fieldname": "voucher_no",
			"label":__("Voucher No"),
			"fieldtype":"Data"
		},
		{
			"fieldname": "voucher_type",
			"label":__("Voucher Type"),
			"fieldtype": "Select",
			"options": ["Purchase Invoice", "Sales Invoice", "Payment Entry"],
			"default": ""
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Select",
			"options":["Customer","Supplier"],
			"default": "",
			on_change: function() {
				frappe.query_report.set_filter_value('party', "")
			}
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "Link",
			"options": "Party",
			get_data: function(txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if(!party_type) return;
				
				return frappe.db.get_list('Party',
					filters = {
						'party_type': party_type
					}
				) 
			}
		}
	]
};
