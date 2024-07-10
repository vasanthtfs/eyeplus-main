// Copyright (c) 2024, Eyeplus and contributors
// For license information, please see license.txt


frappe.query_reports["Sales Person Reports"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 0,
			
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 0,
			"width": "80",
			"default": frappe.datetime.get_today()
		},
        {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "width": "80",
            "options": "Branch" 
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "width": "80",
            "options": "Company" 
        },

	]
};
