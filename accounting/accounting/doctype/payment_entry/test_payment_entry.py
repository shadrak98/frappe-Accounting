# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and Contributors
# See license.txt
from __future__ import unicode_literals
from frappe.utils import flt, nowdate
import frappe
import unittest

class TestPaymentEntry(unittest.TestCase):
	def test_payment_entry_si(self):
		doc_si = create_sales_invoice('Sanji Enterprise', 'Macbook', 1, 50000, True)
		doc_pe = create_payment_entry('Receive','Sales Invoice',doc_si.name)
		check = frappe.db.sql("""SELECT * FROM `tabPayment Entry` WHERE name=%s""",doc_pe.name, as_dict=True)
		self.assertTrue(check,"Payment Entry was not created in test.")
		self.assertEqual(doc_pe.account_paid_from, "Debtors_NP","accounts test fail in PE")
		self.assertEqual(doc_pe.account_paid_to, "Cash_NP","accounts test fail in PE")

	def test_gl_entry(self):
		doc_si = create_sales_invoice('Sanji Enterprise', 'Macbook', 1, 50000, True)
		doc_pe = create_payment_entry('Receive','Sales Invoice', doc_si.name, True)
		gl_entries = get_gl_entries(doc_pe.name)
		self.assertTrue(len(gl_entries) == 2, "GL entries failed")
		dummy = [
			{
				'account':'Debtors_NP',
				'debit':0,
				'credit':50000
			},
			{
				'account':'Cash_NP',
				'debit':50000,
				'credit':0
			}
		]
		self.assertEqual(gl_entries, dummy, "GL entries dnt match.")

def create_sales_invoice(customer, item, quantity, rate, submit=False):
	doc = frappe.new_doc('Sales Invoice')
	doc.customer = customer
	doc.company = 'Noah Perfumes'
	doc.posting_date = nowdate()
	if item:
		doc.set("items",[
			{
				"item_name":item,
				"rate":flt(rate),
				"quantity":quantity
			}
		])
		doc.save()
		if submit:
			doc.submit()
	return doc

def create_payment_entry(pay_type, invoice_type, name, submit=False):
	doc = frappe.new_doc('Payment Entry')
	doc.posting_date = nowdate()
	doc.company = 'Noah Perfumes'
	doc.payment_type = pay_type
	doc.document_type = invoice_type
	doc.document_name = name
	doc.set("payment_reference",[
		{
			"reference_type":invoice_type,
			"reference_name":name
		}
	])
	doc.save()
	if submit:
		doc.submit()

	return doc

def get_gl_entries(voucher):
	return frappe.get_all('GL Entry', filters={'voucher_no':voucher}, fields=['account','debit','credit'])