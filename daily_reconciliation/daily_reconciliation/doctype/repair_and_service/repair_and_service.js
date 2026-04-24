
// frappe.ui.form.on("Repair and Service", {

//     refresh(frm) {

//         // Show POS No only when Entry Type = POS
//         frm.toggle_display("pos_no", frm.doc.entry_type === "POS");

//         // Only after Save
//         if (!frm.doc.__islocal) {

//             // =====================================================
//             // BUTTON 1 : RECEIVE PRODUCT
//             // =====================================================
//             if (!frm.doc.inward_stock_entry) {

//                 frm.add_custom_button("Receive Product", function () {

//                     frappe.confirm(
//                         "Create Stock In Entry for this Repair Job?",
//                         function () {

//                             frappe.call({
//                                 method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_in",
//                                 args: {
//                                     docname: frm.doc.name
//                                 },
//                                 freeze: true,
//                                 freeze_message: "Creating Stock In Entry...",

//                                 callback(r) {

//                                     if (r.message) {

//                                         frappe.show_alert({
//                                             message: "Stock In Created : " + r.message,
//                                             indicator: "green"
//                                         });

//                                         frm.reload_doc();

//                                         frappe.set_route(
//                                             "Form",
//                                             "Stock Entry",
//                                             r.message
//                                         );
//                                     }
//                                 }
//                             });

//                         },
//                         function () {
//                             frappe.show_alert({
//                                 message: "Cancelled",
//                                 indicator: "orange"
//                             });
//                         }
//                     );

//                 }).addClass("btn-primary");
//             }

//             // =====================================================
//             // BUTTON 2 : RETURN TO CUSTOMER
//             // =====================================================
//             if (frm.doc.inward_stock_entry && !frm.doc.outward_stock_entry) {

//                 frm.add_custom_button("Return To Customer", function () {

//                     frappe.confirm(
//                         "Create Stock Out Entry and Deliver Product?",
//                         function () {

//                             frappe.call({
//                                 method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_out",
//                                 args: {
//                                     docname: frm.doc.name
//                                 },
//                                 freeze: true,
//                                 freeze_message: "Creating Stock Out Entry...",

//                                 callback(r) {

//                                     if (r.message) {

//                                         frappe.show_alert({
//                                             message: "Stock Out Created : " + r.message,
//                                             indicator: "green"
//                                         });

//                                         frm.reload_doc();

//                                         frappe.set_route(
//                                             "Form",
//                                             "Stock Entry",
//                                             r.message
//                                         );
//                                     }
//                                 }
//                             });

//                         },
//                         function () {
//                             frappe.show_alert({
//                                 message: "Cancelled",
//                                 indicator: "orange"
//                             });
//                         }
//                     );

//                 }).addClass("btn-success");
//             }
//         }
//     },

//     // =====================================================
//     // ENTRY TYPE CHANGE
//     // =====================================================
//     entry_type(frm) {
//         frm.toggle_display("pos_no", frm.doc.entry_type === "POS");
//     },

//     // =====================================================
//     // FETCH POS DETAILS
//     // =====================================================
//     pos_no(frm) {

//         if (!frm.doc.pos_no) return;

//         frappe.call({
//             method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.get_pos_details",
//             args: {
//                 pos_no: frm.doc.pos_no
//             },

//             freeze: true,
//             freeze_message: "Fetching POS Details...",

//             callback(r) {

//                 if (r.message) {

//                     let d = r.message;

//                     frm.set_value("name1", d.client_name || "");
//                     frm.set_value("phone", d.mobile_number || "");
//                     frm.set_value("address", d.address || "");
//                     frm.set_value("branch", d.branch || "");

//                     frm.set_value("product_name", d.product_name || "");
//                     frm.set_value("sku_code", d.sku_code || "");
//                     frm.set_value("gross_weight", d.gross_weight || 0);
//                     frm.set_value("net_weight", d.net_weight || 0);

//                     frappe.show_alert({
//                         message: "POS Details Loaded",
//                         indicator: "green"
//                     });
//                 }
//             }
//         });
//     }

// });



frappe.ui.form.on("Repair and Service", {

    // =====================================================
    // ON LOAD - SET CURRENT DATE IN DATE FIELD
    // =====================================================
    onload(frm) {
        if (frm.is_new() && !frm.doc.date) {
            frm.set_value("date", frappe.datetime.get_today());
        }
    },

    // =====================================================
    // REFRESH
    // =====================================================
    refresh(frm) {

        // Set current date if blank
        if (frm.is_new() && !frm.doc.date) {
            frm.set_value("date", frappe.datetime.get_today());
        }

        // Show POS No only when Entry Type = POS
        frm.toggle_display("pos_no", frm.doc.entry_type === "POS");

        // Only after Save
        if (!frm.doc.__islocal) {

            // =====================================================
            // BUTTON 1 : RECEIVE PRODUCT
            // =====================================================
            if (!frm.doc.inward_stock_entry) {

                frm.add_custom_button("Receive Product", function () {

                    frappe.confirm(
                        "Create Stock In Entry for this Repair Job?",
                        function () {

                            frappe.call({
                                method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_in",
                                args: {
                                    docname: frm.doc.name
                                },
                                freeze: true,
                                freeze_message: "Creating Stock In Entry...",

                                callback(r) {

                                    if (r.message) {

                                        frappe.show_alert({
                                            message: "Stock In Created : " + r.message,
                                            indicator: "green"
                                        });

                                        frm.reload_doc();

                                        frappe.set_route(
                                            "Form",
                                            "Stock Entry",
                                            r.message
                                        );
                                    }
                                }
                            });

                        },
                        function () {
                            frappe.show_alert({
                                message: "Cancelled",
                                indicator: "orange"
                            });
                        }
                    );

                }).addClass("btn-primary");
            }

            // =====================================================
            // BUTTON 2 : RETURN TO CUSTOMER
            // =====================================================
            if (frm.doc.inward_stock_entry && !frm.doc.outward_stock_entry) {

                frm.add_custom_button("Return To Customer", function () {

                    frappe.confirm(
                        "Create Stock Out Entry and Deliver Product?",
                        function () {

                            frappe.call({
                                method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.make_stock_out",
                                args: {
                                    docname: frm.doc.name
                                },
                                freeze: true,
                                freeze_message: "Creating Stock Out Entry...",

                                callback(r) {

                                    if (r.message) {

                                        frappe.show_alert({
                                            message: "Stock Out Created : " + r.message,
                                            indicator: "green"
                                        });

                                        frm.reload_doc();

                                        frappe.set_route(
                                            "Form",
                                            "Stock Entry",
                                            r.message
                                        );
                                    }
                                }
                            });

                        },
                        function () {
                            frappe.show_alert({
                                message: "Cancelled",
                                indicator: "orange"
                            });
                        }
                    );

                }).addClass("btn-success");
            }
        }
    },

    // =====================================================
    // BEFORE SAVE - FORCE CURRENT DATE
    // =====================================================
    before_save(frm) {
        frm.set_value("date", frappe.datetime.get_today());
    },

    // =====================================================
    // ENTRY TYPE CHANGE
    // =====================================================
    entry_type(frm) {
        frm.toggle_display("pos_no", frm.doc.entry_type === "POS");
    },

    // =====================================================
    // FETCH POS DETAILS
    // =====================================================
    pos_no(frm) {

        if (!frm.doc.pos_no) return;

        frappe.call({
            method: "daily_reconciliation.daily_reconciliation.doctype.repair_and_service.repair_and_service.get_pos_details",
            args: {
                pos_no: frm.doc.pos_no
            },

            freeze: true,
            freeze_message: "Fetching POS Details...",

            callback(r) {

                if (r.message) {

                    let d = r.message;

                    frm.set_value("name1", d.client_name || "");
                    frm.set_value("phone", d.mobile_number || "");
                    frm.set_value("address", d.address || "");
                    frm.set_value("branch", d.branch || "");

                    frm.set_value("product_name", d.product_name || "");
                    frm.set_value("sku_code", d.sku_code || "");
                    frm.set_value("gross_weight", d.gross_weight || 0);
                    frm.set_value("net_weight", d.net_weight || 0);

                    frappe.show_alert({
                        message: "POS Details Loaded",
                        indicator: "green"
                    });
                }
            }
        });
    }

});