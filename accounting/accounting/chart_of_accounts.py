from __future__ import unicode_literals

import frappe
from six import iteritems
from frappe import _
from frappe.utils import cstr
from frappe.utils.nestedset import rebuild_tree

def get_chart(company, abbr):
    chart = {
        _("Application of Funds (Assests)"): {
            _("Current Assets"): {
                _("Accounts Receivable"): {
                    _("Debtors"): {
                        
                    }
                },
                _("Bank Accounts"): {
                    "is_group": 1
                },
                _("Cash In Hand"): {
                    _("Cash"): {
                        
                    }
                },
                _("Stock Assets"): {
                    _("Stock In Hand"): {
                       
                    }
                }
            },
            "account_type": "Asset"
        },
        _("Expenses"): {
            _("Direct Expenses"): {
                _("Stock Expenses"): {
                    _("Cost of Goods Sold"): {
                       
                    }
                },
            },
            "account_type": "Expense"
        },
        _("Income"): {
            _("Direct Income"): {
                _("Sales"): {
                   
                }
            },
            _("Indirect Income"): {
                "is_group": 1
            },
            "account_type": "Income"
        },
        _("Source of Funds (Liabilities)"): {
            _("Capital Account"):{} ,
            _("Current Liabilities"): {
                _("Accounts Payable"): {
                    _("Creditors"): {
                        
                    },
                   
                },
                _("Stock Liabilities"): {
                    _("Stock Received But Not Billed"): {
                    },
                   
                }
            },
            "account_type": "Liability"
        },
    }

    def import_accounts(chart, parent, root_type, root_account=False):
        for name, child in iteritems(chart):
            if(root_account):
                root_type = child.get('account_type')

            if name not in ["account_type", "is_group"]:
                is_group = identify_is_group(child)
                name_with_abbr = name + '_' + abbr
                account = frappe.get_doc({
                    'doctype':'Account',
                    'parent_account': parent,
                    'company':company,
                    'account_type':root_type,
                    'name': name_with_abbr,
                    'account_name': name_with_abbr,
                    'is_group':is_group
                })
                account.insert()

                import_accounts(child, name_with_abbr, root_type, False)

    import_accounts(chart, None, None, True)
    rebuild_tree("Account","parent_account")

def identify_is_group(child):
	if child.get("is_group"):
		is_group = child.get("is_group")
	elif len(set(child.keys())):
		is_group = 1
	else:
		is_group = 0

	return is_group