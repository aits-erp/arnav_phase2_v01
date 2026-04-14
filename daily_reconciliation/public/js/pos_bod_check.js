// frappe.ui.form.on('POS', {
//     before_save: function(frm) {

//         // ✅ Manually enforce branch since it has no reqd:1 in doctype
//         if (!frm.doc.branch) {
//             frappe.throw("Please set a Branch before saving.");
//             return;
//         }

//         frappe.validated = false;

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Daily BOD Entry",
//                 filters: {
//                     date: frappe.datetime.get_today(),  // ✅ BOD date is Date type
//                     warehouse: frm.doc.branch           // ✅ correct field
//                 },
//                 limit_page_length: 1
//             },
//             callback: function(r) {
//                 if (!r.message || r.message.length === 0) {
//                     frappe.msgprint({
//                         title: "BOD Required",
//                         message: `BOD has not been created for Branch '${frm.doc.branch}' today. Please complete BOD entry first.`,
//                         indicator: "red"
//                     });

//                     setTimeout(() => {
//                         frappe.set_route("Form", "Daily BOD Entry", "new-daily-bod-entry-1");
//                     }, 1500);

//                 } else {
//                     frappe.validated = true;
//                     frm.save();
//                 }
//             }
//         });
//     }
// });



frappe.ui.form.on('POS', {

    // ✅ Fires when form loads — but branch may be empty on new form
    // So we handle BOTH refresh and branch field change
    refresh: function(frm) {
        if (frm.is_new()) {
            // ✅ Small delay to let default values populate first
            setTimeout(function() {
                if (frm.doc.branch) {
                    check_bod(frm);
                } else {
                    // Branch not set yet — show a soft warning
                    frappe.show_alert({
                        message: __("Please select a Branch to verify BOD status."),
                        indicator: "orange"
                    }, 5);
                }
            }, 800);
        }
    },

    // ✅ This is the KEY trigger — fires when user selects/changes branch
    branch: function(frm) {
        if (frm.is_new() && frm.doc.branch) {
            check_bod(frm);
        }
    }
});

// ✅ Core BOD check function
function check_bod(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Daily BOD Entry",
            filters: {
                date: frappe.datetime.get_today(),
                warehouse: frm.doc.branch
            },
            limit_page_length: 1
        },
        callback: function(r) {
            if (!r.message || r.message.length === 0) {

                // ✅ Clear popup alert when BOD is missing
                frappe.msgprint({
                    title: __("⚠️ BOD Not Completed"),
                    message: `
                        <div style="padding:10px 0">
                            <p><b>BOD (Beginning of Day) has not been filled for:</b></p>
                            <ul>
                                <li><b>Branch:</b> ${frm.doc.branch}</li>
                                <li><b>Date:</b> ${frappe.datetime.get_today()}</li>
                            </ul>
                            <p style="color:#d32f2f;">
                                You cannot proceed with POS until BOD is completed.
                            </p>
                            <br>
                            <button 
                                class="btn btn-danger btn-sm"
                                onclick="frappe.set_route('Form', 'Daily BOD Entry', 'new-daily-bod-entry-1')">
                                📋 Fill BOD Now
                            </button>
                        </div>
                    `,
                    indicator: "red"
                });

            } else {
                // ✅ BOD found — show green success alert
                frappe.show_alert({
                    message: __("✅ BOD verified for Branch: " + frm.doc.branch),
                    indicator: "green"
                }, 4);
            }
        }
    });
}