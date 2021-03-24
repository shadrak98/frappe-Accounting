# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry

class PurchaseReceipt(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calculate_total()
	
	def on_submit(self):
		default_inventory_account = frappe.get_value('Company', self.company, 'default_inventory_account')
		stock_received_but_not_billed = frappe.get_value('Company',self.company, 'stock_received_but_not_billed')
		make_gl_entry(self, default_inventory_account, self.total_amount, flt(0))
		make_gl_entry(self, stock_received_but_not_billed, flt(0), self.total_amount)

	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)
	
	def validate_quantity(self):
		for itm in self.items:
			if itm.quantity < 0 or itm.quantity == 0:
				frappe.throw("Quantity should be more than 0.")

	def calculate_total(self):
		self.total_quantity, self.total_amount = 0, 0
		if not self.items:
			frappe.throw("There are no items to be saved.")
		for d in self.items:
			d.amount = d.quantity * d.rate
		for d in self.items:
			self.total_amount = flt(self.total_amount) + flt(d.amount)
			self.total_quantity = self.total_quantity + d.quantity

@frappe.whitelist()
def get_purchase_order_items(name=None):
	parent = frappe.get_doc('Purchase Order', name)
	return parent.item