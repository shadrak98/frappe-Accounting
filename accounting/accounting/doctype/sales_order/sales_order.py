# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SalesOrder(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calculate_total()

	def validate_quantity(self):
		for d in items:
			if d.quantity < 0 or d.quantity == 0:
				frappe.throw("Quantity should be more than 0.")

	def calculate_total(self):
		self.total_amount, self.total_quantity = 0, 0
		if not self.items:
			frappe.throw("There are no items to save.")
		for d in self.items:
			d.amount = d.rate * d.quantity
		for d in self.items:
			self.total_amount = self.total_amount + d.amount
			self.total_quantity = self.total_quantity + d.quantity
