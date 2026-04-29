// frappe.ui.form.on("Repair and Service", {

//     // ===============================
//     // ON LOAD
//     // ===============================
//     onload(frm) {
//         if (frm.is_new() && !frm.doc.date) {
//             frm.set_value("date", frappe.datetime.get_today());
//         }
//     },

//     // ===============================
//     // BEFORE SAVE
//     // ===============================
//     before_save(frm) {
//         if (!frm.doc.date) {
//             frm.set_value("date", frappe.datetime.get_today());
//         }
//     },

//     // ===============================
//     // REFRESH
//     // ===============================
//     refresh(frm) {

//         frm.clear_custom_buttons();

//         // Show POS only when needed
//         frm.toggle_display("pos_no", frm.doc.entry_type === "POS");

//         if (!frm.doc.__islocal) {

//             // ===============================
//             // RECEIVE PRODUCT
//             // ===============================
//             if (!frm.doc.inward_stock_entry) {

//                 frm.add_custom_button("Receive Product", () => {

//                     frappe.confirm("Create Stock In Entry?", () => {

//                         frappe.call({
//                             method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_in",
//                             args: { docname: frm.doc.name },
//                             freeze: true,
//                             freeze_message: "Creating Stock In...",

//                             callback(r) {

//                                 if (r.exc) {
//                                     console.error(r.exc);
//                                     frappe.msgprint("Error creating Stock Entry");
//                                     return;
//                                 }

//                                 frappe.show_alert({
//                                     message: "Stock In Created: " + r.message,
//                                     indicator: "green"
//                                 });

//                                 frm.reload_doc();
//                                 frappe.set_route("Form", "Stock Entry", r.message);
//                             }
//                         });

//                     });

//                 }).addClass("btn-primary");
//             }

//             // ===============================
//             // RETURN PRODUCT
//             // ===============================
//             if (frm.doc.inward_stock_entry && !frm.doc.outward_stock_entry) {

//                 frm.add_custom_button("Return To Customer", () => {

//                     frappe.confirm("Create Stock Out Entry?", () => {

//                         frappe.call({
//                             method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_out",
//                             args: { docname: frm.doc.name },
//                             freeze: true,
//                             freeze_message: "Creating Stock Out...",

//                             callback(r) {

//                                 if (r.exc) {
//                                     console.error(r.exc);
//                                     frappe.msgprint("Error creating Stock Entry");
//                                     return;
//                                 }

//                                 frappe.show_alert({
//                                     message: "Stock Out Created: " + r.message,
//                                     indicator: "green"
//                                 });

//                                 frm.reload_doc();
//                                 frappe.set_route("Form", "Stock Entry", r.message);
//                             }
//                         });

//                     });

//                 }).addClass("btn-success");
//             }

//             // ===============================
//             // VIEW LEDGER
//             // ===============================
//             if (frm.doc.inward_stock_entry && frm.doc.outward_stock_entry) {

//                 frm.add_custom_button("View Stock Ledger", () => {

//                     frappe.set_route("query-report", "Stock Ledger", {
//                         voucher_no: ["in", [
//                             frm.doc.inward_stock_entry,
//                             frm.doc.outward_stock_entry
//                         ]]
//                     });

//                 }).addClass("btn-info");
//             }
//         }
//     },

//     // ===============================
//     // ENTRY TYPE CHANGE
//     // ===============================
//     entry_type(frm) {
//         frm.toggle_display("pos_no", frm.doc.entry_type === "POS");
//     },

//     // ===============================
//     // FETCH POS DETAILS (MULTI SKU)
//     // ===============================
//     pos_no(frm) {

//         if (!frm.doc.pos_no) return;

//         frappe.call({
//             method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.get_pos_details",
//             args: { pos_no: frm.doc.pos_no },
//             freeze: true,
//             freeze_message: "Fetching POS Data...",

//             callback(r) {

//                 if (r.exc) {
//                     console.error(r.exc);
//                     frappe.msgprint("Server Error");
//                     return;
//                 }

//                 if (!r.message) {
//                     frappe.msgprint("No POS data found");
//                     return;
//                 }

//                 let d = r.message;

//                 // HEADER
//                 frm.set_value("name1", d.client_name || "");
//                 frm.set_value("phone", d.mobile_number || "");
//                 frm.set_value("address", d.address || "");
//                 frm.set_value("branch", d.branch || "");

//                 // CLEAR TABLE
//                 frm.clear_table("custom_repair_and_service_sku_details");

//                 // ADD MULTIPLE ITEMS
//                 (d.items || []).forEach(item => {

//                     let row = frm.add_child("custom_repair_and_service_sku_details");

//                     row.product_name = item.product_name || "";
//                     row.sku_code = item.sku_code || "";
//                     row.gross_weight = item.gross_weight || 0;
//                     row.net_weight = item.net_weight || 0;
//                 });

//                 frm.refresh_field("custom_repair_and_service_sku_details");

//                 frappe.show_alert({
//                     message: "POS Items Loaded",
//                     indicator: "green"
//                 });
//             }
//         });
//     }

// });



frappe.ui.form.on("Repair and Service", {

    // ===============================
    // ON LOAD
    // ===============================
    onload(frm) {
        if (frm.is_new() && !frm.doc.date) {
            frm.set_value("date", frappe.datetime.get_today());
        }
    },

    // ===============================
    // BEFORE SAVE
    // ===============================
    before_save(frm) {
        if (!frm.doc.date) {
            frm.set_value("date", frappe.datetime.get_today());
        }
    },

    // ===============================
    // REFRESH
    // ===============================
    refresh(frm) {

        frm.clear_custom_buttons();

        frm.toggle_display("pos_no", frm.doc.entry_type === "POS");

        if (!frm.doc.__islocal) {

            // ===============================
            // RECEIVE PRODUCT
            // ===============================
            if (!frm.doc.inward_stock_entry) {

                frm.add_custom_button("Receive Product", () => {

                    frappe.confirm("Create Stock In Entry?", () => {

                        frappe.call({
                            method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_in",
                            args: { docname: frm.doc.name },
                            freeze: true,
                            freeze_message: "Creating Stock In...",

                            callback(r) {
                                if (r.exc) {
                                    frappe.msgprint("Error creating Stock Entry");
                                    return;
                                }

                                frappe.show_alert({
                                    message: "Stock In Created: " + r.message,
                                    indicator: "green"
                                });

                                frm.reload_doc();
                                frappe.set_route("Form", "Stock Entry", r.message);
                            }
                        });

                    });

                }).addClass("btn-primary");
            }

            // ===============================
            // RETURN PRODUCT WITH POPUP + CONFIRM
            // ===============================
            if (frm.doc.inward_stock_entry && !frm.doc.outward_stock_entry) {

                frm.add_custom_button("Return To Customer", () => {

                    let d = new frappe.ui.Dialog({
                        title: "Repair Charges & Payment",
                        fields: [
                            {
                                label: "Repair Charges",
                                fieldname: "repair_charges",
                                fieldtype: "Currency",
                                reqd: 1
                            },
                            {
                                label: "Payment Mode",
                                fieldname: "payment_mode",
                                fieldtype: "Select",
                                options: "Cash\nUPI\nCard\nBank Transfer",
                                reqd: 1
                            },
                            {
                                label: "Paid Amount",
                                fieldname: "paid_amount",
                                fieldtype: "Currency",
                                reqd: 1
                            }
                        ],

                        primary_action_label: "Proceed",

                        primary_action(values) {

                            // ===============================
                            // VALIDATION
                            // ===============================
                            if (!values.repair_charges || !values.payment_mode || !values.paid_amount) {
                                frappe.msgprint("Please fill all fields");
                                return;
                            }

                            if (values.paid_amount < values.repair_charges) {
                                frappe.msgprint("Paid amount cannot be less than charges");
                                return;
                            }

                            d.hide();

                            // ===============================
                            // SECOND CONFIRMATION
                            // ===============================
                            frappe.confirm(
                                "Are you sure you want to Return Product to Customer?",
                                () => {

                                    frappe.call({
                                        method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_out",
                                        args: {
                                            docname: frm.doc.name,
                                            repair_charges: values.repair_charges,
                                            payment_mode: values.payment_mode,
                                            paid_amount: values.paid_amount
                                        },
                                        freeze: true,
                                        freeze_message: "Processing Return...",

                                        callback(r) {

                                            if (r.exc) {
                                                frappe.msgprint("Error creating Stock Entry");
                                                return;
                                            }

                                            frappe.show_alert({
                                                message: "Returned Successfully",
                                                indicator: "green"
                                            });

                                            frm.reload_doc();
                                            frappe.set_route("Form", "Stock Entry", r.message);
                                        }
                                    });

                                }
                            );
                        }
                    });

                    d.show();

                }).addClass("btn-success");
            }

            // ===============================
            // VIEW LEDGER
            // ===============================
            if (frm.doc.inward_stock_entry && frm.doc.outward_stock_entry) {

                frm.add_custom_button("View Stock Ledger", () => {

                    frappe.set_route("query-report", "Stock Ledger", {
                        voucher_no: ["in", [
                            frm.doc.inward_stock_entry,
                            frm.doc.outward_stock_entry
                        ]]
                    });

                }).addClass("btn-info");
            }
        }
    },

    // ===============================
    // ENTRY TYPE
    // ===============================
    entry_type(frm) {
        frm.toggle_display("pos_no", frm.doc.entry_type === "POS");
    },

    // ===============================
    // POS FETCH
    // ===============================
    pos_no(frm) {

        if (!frm.doc.pos_no) return;

        frappe.call({
            method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.get_pos_details",
            args: { pos_no: frm.doc.pos_no },
            freeze: true,
            freeze_message: "Fetching POS Data...",

            callback(r) {

                if (!r.message) return;

                let d = r.message;

                frm.set_value("name1", d.client_name || "");
                frm.set_value("phone", d.mobile_number || "");
                frm.set_value("address", d.address || "");
                frm.set_value("branch", d.branch || "");

                frm.clear_table("custom_repair_and_service_sku_details");

                (d.items || []).forEach(item => {
                    let row = frm.add_child("custom_repair_and_service_sku_details");

                    row.product_name = item.product_name || "";
                    row.sku_code = item.sku_code || "";
                    row.gross_weight = item.gross_weight || 0;
                    row.net_weight = item.net_weight || 0;
                });

                frm.refresh_field("custom_repair_and_service_sku_details");
            }
        });
    }
});