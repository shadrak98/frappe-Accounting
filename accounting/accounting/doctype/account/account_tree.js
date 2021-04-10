frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Account"] = {
    breadcrumb: "Accounts",
    title: __("Chart of Accounts"),
    
    
    filters:[
        {
            fieldname:"company",
            fieldtype:"Link",
            options:"Company",
            label:__("Company"),
            default: frappe.defaults.get_user_default("company")
        }
                   
    ],
    root_label: "Accounts",
	get_tree_nodes: 'accounting.accounting.doctype.account.account.get_children',

}