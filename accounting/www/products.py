import frappe

def get_context(context):
    context.items = frappe.get_list('Item', fields=['item_name','item_rate','route'],ignore_permissions=True)
    return context