# Copyright (c) 2024, Eyeplus and contributors
# For license information, please see license.txt

import frappe

def sum_sales_order(sales_person,from_date=None,to_date=None):
		if from_date and to_date: 
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled' AND (transaction_date>='{from_date}' AND transaction_date<='{to_date}'); """, as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'; """, as_list=True)
		
		return len(query)

def sum_sales_invoice(sales_person,from_date=None,to_date=None):
		if from_date and to_date:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Invoice` si WHERE parenttype = 'Sales Invoice' AND st.parent=si.name AND st.sales_person = '{sales_person}' AND si.status != 'Cancelled' AND (si.posting_date>='{from_date}' AND si.posting_date<='{to_date}');""", as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabSales Invoice` si WHERE parenttype = 'Sales Invoice' AND st.parent=si.name AND st.sales_person = '{sales_person}' AND si.status != 'Cancelled'; """, as_list=True)
		return len(query)
def sum_delivery_note(sales_person,from_date=None,to_date=None):
		if from_date and to_date:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabDelivery Note` dn WHERE parenttype = 'Delivery Note' AND st.parent=dn.name AND st.sales_person = '{sales_person}' AND dn.status != 'Cancelled' AND (dn.posting_date>='{from_date}' AND dn.posting_date<='{to_date}'); """, as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT parent FROM `tabSales Team` st , `tabDelivery Note` dn WHERE parenttype = 'Delivery Note' AND st.parent=dn.name AND st.sales_person = '{sales_person}' AND dn.status != 'Cancelled'; """, as_list=True)
		return len(query)

def total_amount(sales_person,from_date=None,to_date=None):
		if from_date and to_date:
				query = frappe.db.sql(f""" SELECT sum(total) FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled' AND (transaction_date>='{from_date}' AND transaction_date<='{to_date}'); """, as_list=True)
		else:
				query = frappe.db.sql(f""" SELECT  sum(total) FROM `tabSales Team` st , `tabSales Order` so WHERE parenttype = 'Sales Order' AND st.parent=so.name AND st.sales_person = '{sales_person}' AND so.status != 'Cancelled'; """, as_list=True)
		print(query)
		amount = [i[0] for i in query]
		if amount:
				return amount[0]
		else:
				return 0 
		
		
def execute(filters=None):
	data = filters
	print(data)
	from_date  = None
	to_date = None 
	branch = None 
	company = None 
	if data:
			if 'from_date' in data:
					from_date = data['from_date']
			if 'to_date' in data:
					to_date = data['to_date']
			if 'branch' in data:
					branch = data['branch']
			if 'company' in data:
					company = data['company']



	columns = [
		{"label":"Sales Person","fieldname":"sales_person","width":"130"},
		{"label":"Sales Order","fieldname":"sales_order","width":"130"},
		{"label":"Sales Invoice","fieldname":"sales_invoice","width":"130"},
		# {"label":"Payment Entry","fieldname":"payment","width":"130"},
		{"label":"Delivery Note","fieldname":"delivery_note","width":"130"},
		{"label":"Total Amount","fieldname":"total_amount","width":"130"}
		# {"label":"Branch","fieldname":"branch","width":"130"}
		
	]
	data = []
	
	sales_person_query = frappe.db.sql(""" SELECT name FROM `tabSales Person` """,as_list = True)
	sales_person_list = [sp[0] for sp in sales_person_query if sp[0] != "Sales Team"]
	if sales_person_query:
			for sales_person in sales_person_list:
					report_data = []
					report_data.append(sales_person)
					report_data.append(sum_sales_order(sales_person,from_date,to_date))
					report_data.append(sum_sales_invoice(sales_person,from_date,to_date))
					report_data.append(sum_delivery_note(sales_person,from_date,to_date))
					report_data.append(total_amount(sales_person,from_date,to_date))		
					data.append(report_data)		



					
					

	return columns, data
