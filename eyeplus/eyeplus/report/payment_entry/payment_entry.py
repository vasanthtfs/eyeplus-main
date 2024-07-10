# Copyright (c) 2024, Eyeplus and contributors
# For license information, please see license.txt


import frappe

def payment_mode(branch,query_args = None):
	if query_args:
			payment_mode_query = frappe.db.sql(f"SELECT mode_of_payment, SUM(paid_amount) AS 'amount' FROM `tabPayment Entry` WHERE branch ='{branch}' {query_args} GROUP BY mode_of_payment WITH ROLLUP;", as_dict=True)
	else:
			payment_mode_query = frappe.db.sql(f"SELECT mode_of_payment, SUM(paid_amount) AS 'amount' FROM `tabPayment Entry` WHERE branch ='{branch}'  GROUP BY mode_of_payment WITH ROLLUP ;", as_dict=True)

	if payment_mode_query:
		payment_mode = [payment['mode_of_payment'] for payment in payment_mode_query]
		sum_amount = [amount['amount'] for amount in payment_mode_query]
		return payment_mode, sum_amount

def execute(filters=None):
	columns = [
		{
			"label": "Branch",
			"fieldname": "branch",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Payment Mode",
			"fieldname": "payment_mode",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Amount",
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 150
		}
	]


	data = []
	query_branch = frappe.db.sql("SELECT name FROM `tabBranch`", as_list=True)
	branch_name = [i[0] for i in query_branch]
	filter_data = filters
	query_args = ""
	if filter_data:
		if 'from_date' in filter_data:
				from_date = filter_data['from_date']
				query_args += f" AND posting_date >= '{from_date}' "
	if 'to_date' in filter_data:
				to_date = filter_data['to_date']
				query_args += f" AND posting_date <= '{to_date}' "
	if 'company' in filter_data:
				company = filter_data['company']
				query_args += f" AND company = '{company}' "

	for branch in branch_name:
		result = payment_mode(branch,query_args)
		if result is not None:
				pay_mode, pay_amount = result
		else:
				pay_mode = pay_amount = None
				
		if pay_amount:
			amount = sum(pay_amount)
			data.append({"branch": branch, "payment_mode": "", "amount": amount, "indent": 0})
		else:
			data.append({"branch": branch, "payment_mode": "", "amount": None, "indent": 0})
			
		
		if pay_mode:
			for i in range(len(pay_mode)):
				data.append({"branch": "", "payment_mode": pay_mode[i], "amount": pay_amount[i], "indent": 1})

	return columns, data
