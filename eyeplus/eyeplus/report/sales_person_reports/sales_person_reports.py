# Copyright (c) 2024, Eyeplus and contributors
# For license information, please see license.txt



import frappe

def sum_sales_order(sales_person,query_args_so=None):
		if query_args_so: 
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'  {query_args_so} ;""", as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'; """, as_list=True)
		
		return len(query)

def sum_sales_invoice(sales_person,query_args_si=None):
		if query_args_si:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Invoice` si WHERE parenttype = 'Sales Invoice' AND st.parent=si.name AND st.sales_person = '{sales_person}' AND si.status != 'Cancelled' {query_args_si} ;""", as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Invoice` si WHERE parenttype = 'Sales Invoice' AND st.parent=si.name AND st.sales_person = '{sales_person}' AND si.status != 'Cancelled'; """, as_list=True)
		return len(query)
def sum_delivery_note(sales_person,query_args_dn=None):
		if query_args_dn:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabDelivery Note` dn WHERE parenttype = 'Delivery Note' AND st.parent=dn.name AND st.sales_person = '{sales_person}' AND dn.status != 'Cancelled' {query_args_dn} ; """, as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabDelivery Note` dn WHERE parenttype = 'Delivery Note' AND st.parent=dn.name AND st.sales_person = '{sales_person}' AND dn.status != 'Cancelled'; """, as_list=True)
		return len(query)

def total_amount(sales_person,query_args_so=None):
		if query_args_so:
				query = frappe.db.sql(f""" SELECT sum(total) FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled' {query_args_so} ; """, as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT  sum(total) FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'; """, as_list=True)
		# print(query)
		amount = [i[0] for i in query]
		if amount:
				return amount[0]
		else:
				return 0 
def total_amount_wd(sales_person,query_args_so=None):
		amount=[]
		if query_args_so: 
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'  {query_args_so} ;""", as_list=True)
				order = [order_id[0] for order_id in query ]
				order_item_query = frappe.db.sql( """ SELECT parent,item_group,rate  FROM `tabSales Order Item` """,as_list = True)
				if order_item_query:
					order_id = [id[0] for id in order_item_query]
					item_group= [group[1] for group in order_item_query]
					rate = [amount[2] for amount in order_item_query]
					for i in range(len(order_id)):
							if order_id[i] in order:
									if (item_group[i]=="LAPTOP" or item_group[i]=="DESKTOP"or item_group[i]=="LED TV"):
											amount.append(rate[i])


				

		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'; """, as_list=True)
				order = [order_id[0] for order_id in query ]
				order_item_query = frappe.db.sql( """ SELECT parent,item_group,rate  FROM `tabSales Order Item` """,as_list = True)
				if order_item_query:
					order_id = [id[0] for id in order_item_query]
					item_group= [group[1] for group in order_item_query]
					rate = [amount[2] for amount in order_item_query]
					for i in range(len(order_id)):
							if order_id[i] in order:
									if (item_group[i]=="LAPTOP" or item_group[i]=="DESKTOP"or item_group[i]=="LED TV"):
											amount.append(rate[i])

		
		if amount:
				return sum(amount)
		else:
				return 0

	
		
		
def execute(filters=None):
	data = filters
	print(data)
	# from_date  = None
	# to_date = None 
	# branch = None 
	# company = None 
	query_args_so = ""
	query_args_si = ""
	query_args_dn = ""
	
	if data:
			if 'from_date' in data:
					from_date = data['from_date']
					query_args_so += f" AND transaction_date>='{from_date}'"
					query_args_dn += f" AND posting_date>='{from_date}'"
					query_args_si += f" AND posting_date>='{from_date}'"
					
			if 'to_date' in data:
					to_date = data['to_date']
					query_args_so += f" AND transaction_date<='{to_date}'"
					query_args_dn += f" AND posting_date<='{to_date}'"
					query_args_si += f" AND posting_date<='{to_date}'"

			if 'branch' in data:
					branch = data['branch']
					query_args_so += f" AND branch = '{branch}'"
					query_args_si += f" AND branch = '{branch}'"
					query_args_dn += f" AND custom_branch = '{branch}'"
			if 'company' in data:
					company = data['company']
					query_args_so += f" AND company = '{company}'"
					query_args_si += f" AND company = '{company}'"
					query_args_dn += f" AND company = '{company}'"



	columns = [
		{"label":"Sales Person","fieldname":"sales_person","width":"130"},
		{"label":"Sales Order","fieldname":"sales_order","width":"130"},
		{"label":"Sales Invoice","fieldname":"sales_invoice","width":"130"},
		# {"label":"Payment Entry","fieldname":"payment","width":"130"},
		{"label":"Delivery Note","fieldname":"delivery_note","width":"130"},
		{"label":"Total Amount Without Deduction","fieldname":"total_amount","width":"130"},
		{"label":"Total Amount With Deduction","fieldname":"amount_wd","width":"130"}
		
	]
	data = []
	
	sales_person_query = frappe.db.sql(""" SELECT name FROM `tabSales Person` """,as_list = True)
	sales_person_list = [sp[0] for sp in sales_person_query if sp[0] != "Sales Team"]
	if sales_person_query:
			for sales_person in sales_person_list:
					# print(sales_person)
					report_data = []
					report_data.append(sales_person)
					report_data.append(sum_sales_order(sales_person,query_args_so))
					report_data.append(sum_sales_invoice(sales_person,query_args_si))
					report_data.append(sum_delivery_note(sales_person,query_args_dn))
					report_data.append(total_amount(sales_person,query_args_so))	
					report_data.append(total_amount_wd(sales_person,query_args_so))	
					data.append(report_data)		



					
					

	return columns, data

