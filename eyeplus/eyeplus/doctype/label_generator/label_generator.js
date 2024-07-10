function set_read_only(frm, isOldDocument){
	frm.set_df_property("receipt_id", "read_only", isOldDocument);
	frm.set_df_property("item_code", "read_only", isOldDocument);
	frm.set_df_property("total_serial_no", "read_only", isOldDocument);
	frm.set_df_property("serial_no", "read_only", isOldDocument);
	frm.set_df_property("from_no", "read_only", isOldDocument);
	frm.set_df_property("to_no", "read_only", isOldDocument);
}

frappe.ui.form.on('Label Generator', {
	refresh: function(frm) {
		var isOldDocument = frm.doc.__islocal ? 0 : 1;
		set_read_only(frm, isOldDocument)
		set_css(frm)
		frm.set_query("receipt_id", function(){
			if(frm.doc.item_code == null){
				frappe.throw("Need to enter item code")
				return
			}
			return {
				"filters": [
					["Purchase Receipt Item", "item_code", "in", frm.doc.item_code],
					["Purchase Receipt", "status", "=", "To Bill"]
				]
			}
		});
	},

	fetch_serial_no: function(frm) {
		frappe.call({
			method:"eyeplus.eyeplus.doctype.label_generator.label_generator.fetch_serial_no",
			args:{ 'receipt_id' : frm.doc.receipt_id, 'item_code': frm.doc.item_code},
			callback: function(r){
				var items = String(r.message).split('\n')
				frm.doc.total_serial_no = items.length;
				frm.refresh_field('total_serial_no');

				frm.clear_table("serial_no");
				items.forEach((item) => {
					var serial_row = frm.fields_dict.serial_no.grid.add_new_row();
					frappe.model.set_value(serial_row.doctype, serial_row.name, "serial_no", item);
				})
			}
		})
}})

// print: function(frm){
// 	frappe.set_route('print','Label Generator', frm.doc.name)
// }
// });

frappe.ui.form.on("Label Generator", "onload", function(frm){
	set_css(frm)
	set_read_only(frm)
    frm.set_query("receipt_id", function(){
		return {
			"filters": [
				["Purchase Receipt Item", "item_code", "in", frm.doc.item_code],
				["Purchase Receipt", "status", "=", "To Bill"]
			]
		}
	});
});

frappe.ui.form.on("Label Generator", "onload", function(frm){
    frm.set_query("print_format", function(){
		return {
			"filters": [
				["Print Format", "doc_type", "in", "Label Generator"],
			]
		}
	});
});

frappe.ui.form.on("Label Generator", "refresh", function(frm){
    frm.set_query("print_format", function(){
		return {
			"filters": [
				["Print Format", "doc_type", "in", "Label Generator"],
			]
		}
	});
});


var set_css = function(frm){
    document.querySelectorAll("[data-fieldname='fetch_serial_no']")[1].style.backgroundColor ="#2490EF";
    document.querySelectorAll("[data-fieldname='fetch_serial_no']")[1].style.color ="white"; 
}