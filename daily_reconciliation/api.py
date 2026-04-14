import frappe
from frappe.utils import today

def validate_bod_before_pos(doc, method):

    branch = doc.get("branch")  # ✅ correct fieldname from your POS doctype

    if not branch:
        frappe.throw("Please set a Branch (Warehouse) on the POS entry before saving.")
        return

    bod_exists = frappe.db.exists("Daily BOD Entry", {
        "date": today(),       # ✅ correct — your BOD date field is "date"
        "warehouse": branch    # ✅ correct — your BOD warehouse field is "warehouse"
    })

    if not bod_exists:
        frappe.throw(
            f"BOD has not been created for Branch '{branch}' today. "
            f"Please complete the BOD entry first."
        )


# 🔹 EOD Reminder: Send alert at 6:10 PM
def send_eod_reminder():

    warehouses = frappe.get_all("Warehouse", pluck="name")

    # Get all active users (instead of hardcoded email)
    users = frappe.get_all("User", filters={"enabled": 1}, pluck="email")

    for wh in warehouses:

        eod_exists = frappe.db.exists("Daily EOD Entry", {
            "date": today(),
            "warehouse": wh
        })

        if not eod_exists:
            frappe.sendmail(
                recipients=users,
                subject="EOD Pending Reminder",
                message=f"EOD not completed for Warehouse: {wh}"
            )