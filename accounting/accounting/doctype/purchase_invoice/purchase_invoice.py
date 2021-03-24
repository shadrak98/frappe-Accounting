# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry

class PurchaseInvoice(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calculate_total()

	def on_submit(self):
		default_payable_account = frappe.get_value('Company', self.company, 'default_payable_account')
		stock_received_but_not_billed = frappe.get_value('Company', self.company, 'stock_received_but_not_billed')
		make_gl_entry(self,stock_received_but_not_billed,self.total_amount, flt(0))
		make_gl_entry(self,default_payable_account,flt(0),self.total_amount)

	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)
	
	def validate_quantity(self):
		for d in self.items:
			if d.quantity < 0 or d.quantity == 0:
				frappe.throw("Item Quantity should more than 0.")
	
	def calculate_total(self):
		self.total_amount, self.total_quantity = 0, 0
		if not self.items:
			frappe.throw("There are no items to save.")
		for d in self.items:
			d.amount = d.quantity * d.rate
		for d in self.items:
			self.total_amount = flt(self.total_amount) + flt(d.amount)
			self.total_quantity = self.total_quantity + f.quantity

@frappe.whitelist
def get_purchase_receipt_items(name=None):
	parent = frappe.get_doc('Purchase Receipt', name)
	return parent.items
