# Copyright (c) 2013, shadrak and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
	
	company = filters.get('company')
	account = filters.get('account')
	voucher_no = filters.get('voucher_no')
	voucher_type = filters.get('voucher_type')
	party = filters.get('party')
	party_type = filters.get('party_type')
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')

	data = frappe.db.sql("""
	SELECT
		posting_date, party, party_type, account, debit, credit, company, voucher_type, voucher_no
	FROM 
		`tabGL Entry`
	WHERE
		{conditions}
	ORDER BY
		posting_date
	""".format(conditions = get_conditions(filters)), filters, as_dict = 1)

	return data

def get_columns():
	return [
		"Posting Date:Date:110",
		"Party:Link/Party:180",
		"Party Type:Data:120",
		"Account:Link/Account:150",
		"Debit:Currency:90",
		"Credit:Currency:90",
		"Company:Link/Company:150",
		"Voucher Type:Data:150",
		"Voucher No:Data:150"
	]

def get_conditions(filters):
	conditions = []

	if filters.get("account"):
		lft, rgt = frappe.db.get_value("Account", filters["account"], ["lft", "rgt"])
		conditions.append("""account in (select name from tabAccount
			where lft>=%s and rgt<=%s and docstatus<2)""" % (lft, rgt))

	conditions.append("(posting_date >= %(from_date)s and posting_date <= %(to_date)s)")

	if filters.get("company"):
		conditions.append("company=%(company)s")
	
	if filters.get("party_type"):
		conditions.append("party_type=%(party_type)s")

	if filters.get("party"):
		conditions.append("party in %(party)s")

	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")

	if filters.get("voucher_type"):
		conditions.append("voucher_type=%(voucher_type)s")

	return "{}".format(" and ".join(conditions)) if conditions else ""