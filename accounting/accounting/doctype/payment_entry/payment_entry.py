# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt

class PaymentEntry(Document):
	def validate(self):
		self.amount = 0
		for d in self.payment_references:
			self.amount = self.amount + flt(d.amount)
		if self.payment_type == "Pay":
			account_paid_to = frappe.get_value('Company',self.company,'default_payable_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_cash_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
		elif self.payment_type == "Receive":
			ccount_paid_to = frappe.get_value('Company',self.company,'default_cash_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_receivable_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from

	def on_submit(self):
		if self.payment_type == "Pay":
			account_paid_to = frappe.get_value('Company',self.company,'default_payable_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_cash_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
			make_gl_entry(self,self.account_paid_to,self.amount,flt(0))
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount)
		else:
			account_paid_to = frappe.get_value('Company',self.company,'default_cash_account')
			account_paid_from = frappe.get_value('Company',self.company,'default_receivable_account')
			self.account_paid_to = account_paid_to
			self.account_paid_from  = account_paid_from
			make_gl_entry(self,self.account_paid_to,self.amount,flt(0))
			make_gl_entry(self,self.account_paid_from,flt(0),self.amount)


	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)
