# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and Contributors
# See license.txt
from __future__ import unicode_literals
from frappe.utils import flt, nowdate
import frappe
import unittest

class TestSalesInvoice(unittest.TestCase):
	def test_sales_invoice(self):
		doc = create_new_invoice('Sanji Enterprise', 'Macbook', 1, 50000)
		doc.append("items",{
			"item_name": 'Macbook',
			"rate": 50000,
			"quantity": 1
		})
		doc.save()
		check = frappe.db.sql("""SELECT * FROM `tabSales Invoice` WHERE name=%s""",doc.name, as_dict=True)
		self.assertTrue(check,"Invoice not created")
		self.assertEqual(doc.total_amount, 100000, "Totals don't match")
		self.assertEqual(doc.total_quantity, 2, "Total Quantity don't match")

	def test_gl_entry(self):
		doc = create_new_invoice('Administrator', 'Bicycle', 1, 15000, True)
		gl_entries = get_gl_entries(doc.name)
		self.assertTrue(len(gl_entries) == 2, "Creating GL entries failed.")
		dummy = [
			{
				'account':'Sales_NP',
				'debit':0,
				'credit':15000
			},
			{
				'account':'Debtors_NP',
				'debit':15000,
				'credit':0
			}
		]
		self.assertEqual(gl_entries, dummy, "GL entries test failed.")


def create_new_invoice(customer, item, qty, rate, submit = False):
	doc = frappe.new_doc('Sales Invoice')
	doc.company = 'Noah Perfumes'
	doc.customer = customer
	if item:
		doc.set("items",[
			{
				"item_name":item,
				"rate":flt(rate),
				"quantity":qty
			}
		])
		doc.save()
		if submit:
			doc.submit()
	return doc

def get_gl_entries(name):
	return frappe.get_all('GL Entry', filters={'voucher_no':name}, fields=['account', 'debit', 'credit'])
