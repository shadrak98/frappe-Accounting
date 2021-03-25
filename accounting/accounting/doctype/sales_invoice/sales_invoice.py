# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt

class SalesInvoice(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calculate_total()

	def on_submit(self):
		default_receivable_account = frappe.get_value('Company', self.company, 'default_receivable_account')
		default_income_account = frappe.get_value('Company', self.company, 'default_income_account')
		make_gl_entry(self, default_receivable_account, self.total_amount, flt(0))
		make_gl_entry(self, default_income_account, flt(0), self.total_amount)

	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)

	def validate_quantity(self):
		for d in items:
			if d.quantity < 0 or d.quantity == 0:
				frappe.throw("Item quantity should be more than 0.")

	def calculate_total(self):
		self.total_amount, self.total_quantity = 0, 0
		if not self.items:
			frappe.throw("There are no items to be saved. Please add items.")
		for d in self.items:
			d.amount = d.quantity + d.rate 
			self.total_amount = self.total_amount + d.amount
			self.total_quantity = self.total_quantity + d.quantity
