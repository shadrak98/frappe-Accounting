# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt

class DeliveryNote(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calculate_total()

	def on_submit(self):
		default_expense_account = frappe.get_value('Company', self.company, 'default_expense_account')
		default_inventory_account = frappe.get_value('Company', self.company, 'default_inventory_account')
		make_gl_entry(self, default_expense_account, self.total_amount, flt(0))
		make_gl_entry(self, default_inventory_account, flt(0), self.total_amount) 
	
	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)

	def validate_quantity(self):
		for d in self.items:
			if d.item_quantity < 0 or d.item_quantity == 0:
				frappe.throw("Items should be more than 0.")

	def calculate_total(self):
		self.total_amount, self.total_quantity = 0, 0
		if not self.items:
			frappe.throw("There are no items to be saved.")
		for d in self.items:
			d.amount = d.item_quantity * d.item_rate
		for d in self.items:
			self.total_amount = self.total_amount + d.amount
			self.total_quantity = self.total_quantity + d.item_quantity

@frappe.whitelist
def get_sales_order_item(name=None):
	parent = frappe.get_doc('Sales Order',name)
	return parent.items