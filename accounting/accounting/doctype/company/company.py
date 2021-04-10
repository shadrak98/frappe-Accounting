# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.chart_of_accounts import get_chart

class Company(Document):
	def validate(self):
		if not self.abbr:
			names = self.company_name.split()
			abbr_list = []
			for d in names:
				abbr_list.append(d[0])
			abbr = "".join(abbr_list)

			validate_abbr(self,abbr)
			self.set_default_accounts()

	def on_update(self):
		if not frappe.db.sql("""
			SELECT
				name
			FROM
				tabAccount
			WHERE
				company=%s and docstatus<2 limit 1""", self.company_name):
				get_chart(self.company_name, self.abbr)

	def set_default_accounts(self):
		set_default(self, "default_inventory_account", "Stock In Hand")
		set_default(self, "default_cash_account", "Cash")
		set_default(self, "default_payable_account", "Creditors")
		set_default(self, "default_receivable_account", "Debtors")
		set_default(self, "default_income_account", "Sales")
		set_default(self, "default_expense_account", "Cost of Goods Sold")
		set_default(self, "stock_received_but_not_billed", "Stock Received But Not Billed")

def set_default(self, field, name):
	name = name + '-' + self.abbr
	frappe.db.set(self, field, name)

def validate_abbr(self, abbr):
	check = frappe.db.exists({
		"doctype":"Company",
		"abbr": abbr
	})
	if not check:
		self.abbr = abbr
	else:
		frappe.throw("Cannot make a unique abbreviation. Company Name already Exists.")