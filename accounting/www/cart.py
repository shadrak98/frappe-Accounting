import frappe

def get_context(context):
    user = frappe.session.user
    context.user = user
    sin = frappe.db.get_list('Sales Invoice', filters={'docstatus':0, 'customer':user}, ignore_permissions=True)
    if sin:
        doc = frappe.get_doc('Sales Invoice', sin[0]['name'])
    else:
        doc = None
    context.cart = doc
    return context