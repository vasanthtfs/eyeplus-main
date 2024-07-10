# Copyright (c) 2024, Eyeplus and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LabelGenerator(Document):
	def validate(self):
		if(self.receipt_id == None or self.item_code == None):
			frappe.throw("Please enter appropriate values..")

		if(self.from_no == 0):
			frappe.throw("The (from) field should not be 0")
		if(self.to_no == 0):
			frappe.throw("The (to) field should not be 0")
		if(self.from_no > self.to_no):
			frappe.throw("The from_no should not be greater than the to_no")

@frappe.whitelist()
def fetch_serial_no(receipt_id, item_code):
	doc_list = frappe.get_all('Purchase Receipt Item', filters={'parent': receipt_id,'item_code': item_code}, fields = ['serial_no'], ignore_permissions=True)
	return doc_list[0]['serial_no']