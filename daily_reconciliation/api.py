import frappe
from frappe.utils import today, now_datetime, get_datetime

def validate_bod_before_pos(doc, method):

    branch = doc.get("branch")

    if not branch:
        frappe.throw("Please set a Branch before saving.")
        return

    # ✅ BOD date field is a plain Date type so today() works fine for BOD
    # The issue was only on POS side — BOD.date is Date, so this is correct
    bod_exists = frappe.db.exists("Daily BOD Entry", {
        "date": today(),        # ✅ BOD uses Date fieldtype, today() matches correctly
        "warehouse": branch     # ✅ BOD warehouse field confirmed
    })

    if not bod_exists:
        frappe.throw(
            f"BOD has not been created for Branch '{branch}' today. "
            f"Please complete BOD entry first."
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