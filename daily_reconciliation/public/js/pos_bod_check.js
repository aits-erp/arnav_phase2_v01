frappe.ui.form.on('POS Invoice', {
    onload: function(frm) {

        setTimeout(() => {

            let warehouse = frm.doc.set_warehouse;

            if (!warehouse) return;

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Daily BOD Entry",
                    filters: {
                        date: frappe.datetime.get_today(),
                        warehouse: warehouse
                    },
                    limit_page_length: 1
                },
                callback: function(r) {

                    if (!r.message || r.message.length === 0) {

                        frappe.msgprint({
                            title: "BOD Required",
                            message: "Please create BOD before doing POS Entry",
                            indicator: "red"
                        });

                        frappe.set_route("Form", "Daily BOD Entry", "new-daily-bod-entry");

                        frm.disable_save();
                    }
                }
            });

        }, 1000);
    }
});