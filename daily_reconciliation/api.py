import frappe
from frappe.utils import today


# 🔹 POS Restriction: Block POS if BOD not created
def validate_bod_before_pos(doc, method):

    warehouse = doc.set_warehouse

    if not warehouse:
        return

    bod_exists = frappe.db.exists("Daily BOD Entry", {
        "date": today(),
        "warehouse": warehouse
    })

    if not bod_exists:
        frappe.throw(f"BOD not created for Warehouse {warehouse}. Cannot create POS Entry.")


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