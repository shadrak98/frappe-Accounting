# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe.model.document import Document

class PurchaseOrder(Document):
	
	def validate(self):
		self.validate_quantity()
		self.calc_total_amount()

	def validate_quantity(self):
		for i in self.item:
			if i.item_quantity < 0 or i.item_quantity == 0:
				frappe.throw("Quantity should be more than 0.")

	def calc_total_amount(self):
		self.total_amount = 0
		if not self.item:
			frappe.throw("There are no Items to save.")
		for itm in self.item:
			amount = itm.item_quantity * itm.item_rate
			self.total_amount = flt(amount)
