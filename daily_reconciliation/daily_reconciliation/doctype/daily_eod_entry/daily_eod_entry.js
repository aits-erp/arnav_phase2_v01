// Copyright (c) 2026, Sukku and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily EOD Entry", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Daily EOD Entry', {
    refresh: function(frm) {
        if (frm.doc.stock_variance != 0) {
            frappe.msgprint("⚠️ Variance detected. Please review before submitting.");
        }
    }
});