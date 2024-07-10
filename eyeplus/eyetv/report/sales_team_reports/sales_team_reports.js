// Copyright (c) 2024, Eyeplus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Team Reports"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 0,
			"default":"2023-11-09"
			// "default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 0,
			"width": "80",
			"default":"2023-11-09"
			// "default": frappe.datetime.get_today()
		},
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "width": "80",
            "options": "Branch" 
        }

	]
};
