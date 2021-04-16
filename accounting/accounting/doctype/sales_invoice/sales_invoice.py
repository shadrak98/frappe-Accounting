# -*- coding: utf-8 -*-
# Copyright (c) 2021, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting.accounting.general_ledger import make_gl_entry, make_reverse_gl_entry
from frappe.utils import flt, nowdate

class SalesInvoice(Document):
	
	def validate(self):
		validate_quantity(self)
		calculate_total(self)

	def on_submit(self):
		default_receivable_account = frappe.get_value('Company', self.company, 'default_receivable_account')
		default_income_account = frappe.get_value('Company', self.company, 'default_income_account')
		make_gl_entry(self, default_receivable_account, self.total_amount, flt(0))
		make_gl_entry(self, default_income_account, flt(0), self.total_amount)

	def on_cancel(self):
		make_reverse_gl_entry(self, self.doctype, self.name)

def validate_quantity(self):
	for d in self.items:
		if d.quantity < 0 or d.quantity == 0:
			frappe.throw("Item quantity should be more than 0.")

def calculate_total(self):
	self.total_amount, self.total_quantity = 0, 0
	if not self.items:
		frappe.throw("There are no items to be saved. Please add items.")
	for d in self.items:
		d.amount = d.quantity * d.rate 
		self.total_amount = self.total_amount + d.amount
		self.total_quantity = self.total_quantity + d.quantity

@frappe.whitelist
def get_sales_invoice_items(name=None):
	parent = frappe.get_doc('Sales Invoice',name)
	return parent

@frappe.whitelist()
def add_to_cart(user, item_name, quantity):
	data = frappe.get_list('Sales Invoice', filters={'docstatus':0, 'customer':user})
	print("\n\n\n"+str(data)+"\n\n\n")
	if not data:
		print("\n\n\n not data\n\n\n")
		create_sales_invoice(user, item_name, quantity)
	else:
		print("else part")
		doc = frappe.get_doc('Sales Invoice', data[0]['name'])
		doc.append("items",{
			'item_name':item_name,
			'quantity':flt(quantity)
		})
		doc.save()

@frappe.whitelist()
def create_sales_invoice(user, name, quantity,submit=False):
	doc = frappe.new_doc('Sales Invoice')
	doc.customer = user
	doc.company = 'Noah Perfumes'
	doc.set('items',[{
		'item_name':name,
		'quantity': flt(quantity)
	}])
	doc.save()
	if submit:
		doc.submit()

@frappe.whitelist()
def update_cart(user,index,qty = 0,update = False,buy = False, submit = False):
	check = check_cart(user)
	
	cart = frappe.get_doc('Sales Invoice',check[0]['name'])
	cart.posting_date = nowdate()
	if submit:
		cart.submit()
		

	else:
		index = int(index)
		qty = int(qty)
		print(qty)
		for idx,item in enumerate(cart.items):
			
			if idx == index:
				if buy:
					create_sales_invoice(user,item.item_name,item.quantity,submit = True)
				
					
				elif update:
					
					item.quantity = flt(qty)
					break
				cart.remove(item)
				break
		if not len(cart.items):
			frappe.delete_doc('Sales Invoice',check[0]['name'])
		else:
			cart.save()

def check_cart(user):
	
	check = frappe.db.get_list('Sales Invoice',filters = {'docstatus':0,'customer':user})
	return check