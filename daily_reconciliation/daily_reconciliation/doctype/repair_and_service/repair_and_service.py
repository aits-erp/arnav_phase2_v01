
import frappe
from frappe.model.document import Document


class RepairandService(Document):
    pass


# ==========================================================
# GET POS DETAILS
# ==========================================================
@frappe.whitelist()
def get_pos_details(pos_no):

    pos = frappe.get_doc("POS", pos_no)

    item = {}

    if pos.sku_details and len(pos.sku_details) > 0:
        row = pos.sku_details[0]

        item = {
            "product_name": row.product or "",
            "sku_code": row.sku or "",
            "gross_weight": row.gross_weight or 0,
            "net_weight": row.net_weight or 0
        }

    return {
        "client_name": pos.client_name or "",
        "mobile_number": pos.mobile_number or "",
        "address": pos.address or "",
        "branch": pos.branch or "",
        **item
    }


# ==========================================================
# COMMON FUNCTION
# SKU → GET ITEM + BATCH + WAREHOUSE
# ==========================================================
def get_sku_data(sku_code):

    if not sku_code:
        frappe.throw("SKU Code is required")

    sku = frappe.get_doc("SKU", sku_code)

    item_code = sku.product
    batch_no = sku.batch_no
    warehouse = sku.warehouse

    if not item_code:
        frappe.throw(f"Item not linked in SKU : {sku_code}")

    return {
        "item_code": item_code,
        "batch_no": batch_no,
        "warehouse": warehouse
    }


# ==========================================================
# RECEIVE PRODUCT
# ==========================================================
@frappe.whitelist()
def make_stock_in(docname):

    doc = frappe.get_doc("Repair and Service", docname)

    if doc.inward_stock_entry:
        return doc.inward_stock_entry

    data = get_sku_data(doc.sku_code)

    target_warehouse = doc.branch or data["warehouse"]

    if not target_warehouse:
        frappe.throw("Warehouse missing in Repair Form / SKU")

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Receipt"
    se.company = frappe.defaults.get_user_default("Company")

    se.append("items", {
        "item_code": data["item_code"],
        "qty": 1,
        "batch_no": data["batch_no"],
        "t_warehouse": target_warehouse,
        "allow_zero_valuation_rate": 1
    })

    se.insert(ignore_permissions=True)
    se.submit()

    doc.db_set("inward_stock_entry", se.name)
    doc.db_set("repair_status", "In Progress")

    return se.name


# ==========================================================
# RETURN TO CUSTOMER
# ==========================================================
@frappe.whitelist()
def make_stock_out(docname):

    doc = frappe.get_doc("Repair and Service", docname)

    if doc.outward_stock_entry:
        return doc.outward_stock_entry

    if not doc.inward_stock_entry:
        frappe.throw("Please Receive Product First")

    data = get_sku_data(doc.sku_code)

    source_warehouse = doc.branch or data["warehouse"]

    if not source_warehouse:
        frappe.throw("Warehouse missing in Repair Form / SKU")

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.company = frappe.defaults.get_user_default("Company")

    se.append("items", {
        "item_code": data["item_code"],
        "qty": 1,
        "batch_no": data["batch_no"],
        "s_warehouse": source_warehouse,
        "allow_zero_valuation_rate": 1
    })

    se.insert(ignore_permissions=True)
    se.submit()

    doc.db_set("outward_stock_entry", se.name)
    doc.db_set("repair_status", "Delivered")

    return se.name
