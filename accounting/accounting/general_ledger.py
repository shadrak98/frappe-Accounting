from __future__ import unicode_literals
import frappe
from frappe.utils import now

def make_gl_entry(self, account, debit, credit):
    if(self.doctype == "Sales Invoice"):
        party_type = "Customer"
        party = self.customer
    elif (self.doctype == "Purchase Invoice"):
        party_type = "Supplier"
        party = self.supplier
    elif (self.doctype == "Payment Entry"):
        if(self.payment_type == "Receive"):
            party_type = "Customer"
            party = self.party
        else:
            party_type = "Supplier"
            party = self.party
    
    gl_entry = frappe.get_doc({
        'doctype': 'GL Entry',
        'posting_date': self.posting_date,
        'account': account,
        'voucher_type': self.doctype,
        'voucher_no': self.name,
        'debit': debit,
        'credit': credit,
        'company': self.company,
        'party': party,
        'party_type': party_type
    })
    gl_entry.insert()


def make_reverse_gl_entry(self, voucher_type, voucher_no):
    gl_entries = frappe.get_all("GL Entry",
                    fields = ['*'],
                    filters = {
                        "voucher_type": voucher_type,
                        "voucher_no": voucher_no,
                        "is_cancelled": 0
                    })

    if gl_entries:
        set_as_cancel(gl_entries[0]['voucher_type'],gl_entries[0]['voucher_no'])

        for entry in gl_entries:
            entry['name'] = None
            debit = entry.get('debit', 0)
            credit = entry.get('credit', 0)

            entry['debit'] = credit
            entry['credit'] = debit

            entry['is_cancelled'] = 1
            if entry['debit'] or entry['credit']:
                make_reverse_entry(entry)

def make_reverse_entry(entry):
    gle = frappe.new_doc('GL Entry')
    gle.update(entry)
    gle.insert()


def set_as_cancel(voucher_type, voucher_no):
    frappe.db.sql("""UPDATE `tabGL Entry` SET is_cancelled = 1,
                modified=%s, modified_by=%s
                where voucher_type=%s and voucher_no=%s and is_cancelled = 0""",
                (now(), frappe.session.user, voucher_type, voucher_no))