# import frappe
# from frappe.model.document import Document


# class RepairandService(Document):
#     pass


# # ==========================================================
# # GET POS DETAILS
# # ==========================================================
# @frappe.whitelist()
# def get_pos_details(pos_no):

#     pos = frappe.get_doc("POS", pos_no)

#     item = {}

#     if pos.sku_details and len(pos.sku_details) > 0:
#         row = pos.sku_details[0]

#         item = {
#             "product_name": row.product or "",
#             "sku_code": row.sku or "",
#             "gross_weight": row.gross_weight or 0,
#             "net_weight": row.net_weight or 0
#         }

#     return {
#         "client_name": pos.client_name or "",
#         "mobile_number": pos.mobile_number or "",
#         "address": pos.address or "",
#         "branch": pos.branch or "",
#         **item
#     }


# # ==========================================================
# # COMMON FUNCTION
# # SKU → GET ITEM + BATCH + WAREHOUSE
# # ==========================================================
# def get_sku_data(sku_code):

#     if not sku_code:
#         frappe.throw("SKU Code is required")

#     sku = frappe.get_doc("SKU", sku_code)

#     item_code = sku.product
#     batch_no = sku.batch_no
#     warehouse = sku.warehouse

#     if not item_code:
#         frappe.throw(f"Item not linked in SKU : {sku_code}")

#     return {
#         "item_code": item_code,
#         "batch_no": batch_no,
#         "warehouse": warehouse
#     }


# # ==========================================================
# # RECEIVE PRODUCT
# # ==========================================================
# @frappe.whitelist()
# def make_stock_in(docname):

#     doc = frappe.get_doc("Repair and Service", docname)

#     if doc.inward_stock_entry:
#         return doc.inward_stock_entry

#     data = get_sku_data(doc.sku_code)

#     target_warehouse = doc.branch or data["warehouse"]

#     if not target_warehouse:
#         frappe.throw("Warehouse missing in Repair Form / SKU")

#     se = frappe.new_doc("Stock Entry")
#     se.stock_entry_type = "Material Receipt"
#     se.company = frappe.defaults.get_user_default("Company")

#     se.append("items", {
#         "item_code": data["item_code"],
#         "qty": 1,
#         "batch_no": data["batch_no"],
#         "t_warehouse": target_warehouse,
#         "allow_zero_valuation_rate": 1
#     })

#     se.insert(ignore_permissions=True)
#     se.submit()

#     doc.db_set("inward_stock_entry", se.name)
#     doc.db_set("repair_status", "In Progress")

#     return se.name


# # ==========================================================
# # RETURN TO CUSTOMER
# # ==========================================================
# @frappe.whitelist()
# def make_stock_out(docname):

#     doc = frappe.get_doc("Repair and Service", docname)

#     if doc.outward_stock_entry:
#         return doc.outward_stock_entry

#     if not doc.inward_stock_entry:
#         frappe.throw("Please Receive Product First")

#     data = get_sku_data(doc.sku_code)

#     source_warehouse = doc.branch or data["warehouse"]

#     if not source_warehouse:
#         frappe.throw("Warehouse missing in Repair Form / SKU")

#     se = frappe.new_doc("Stock Entry")
#     se.stock_entry_type = "Material Issue"
#     se.company = frappe.defaults.get_user_default("Company")

#     se.append("items", {
#         "item_code": data["item_code"],
#         "qty": 1,
#         "batch_no": data["batch_no"],
#         "s_warehouse": source_warehouse,
#         "allow_zero_valuation_rate": 1
#     })

#     se.insert(ignore_permissions=True)
#     se.submit()

#     doc.db_set("outward_stock_entry", se.name)
#     doc.db_set("repair_status", "Delivered")

#     return se.name




# import frappe
# from frappe.model.document import Document
# from frappe.utils import nowdate


# class RepairandService(Document):
#     pass


# # ==========================================================
# # GET POS DETAILS (MULTI SKU SUPPORT)
# # ==========================================================
# @frappe.whitelist()
# def get_pos_details(pos_no):

#     if not pos_no:
#         return {}

#     pos = frappe.get_doc("POS", pos_no)

#     items = []

#     # ✅ Loop all SKU rows
#     if hasattr(pos, "sku_details") and pos.sku_details:
#         for row in pos.sku_details:

#             items.append({
#                 "product_name": row.product or "",
#                 "sku_code": row.sku or "",
#                 "gross_weight": row.gross_weight or 0,
#                 "net_weight": row.net_weight or 0
#             })

#     return {
#         "client_name": pos.client_name or "",
#         "mobile_number": pos.mobile_number or "",
#         "address": pos.address or "",
#         "branch": pos.branch or "",
#         "items": items   # ✅ IMPORTANT (list, not single item)
#     }


# # ==========================================================
# # COMMON FUNCTION
# # ==========================================================
# def get_sku_data(sku_code):

#     if not sku_code:
#         frappe.throw("SKU Code is required")

#     sku = frappe.get_doc("SKU", sku_code)

#     if not sku.product:
#         frappe.throw(f"Item not linked in SKU : {sku_code}")

#     return {
#         "item_code": sku.product,
#         "batch_no": sku.batch_no,
#         "warehouse": sku.warehouse
#     }


# # ==========================================================
# # STOCK IN (MULTIPLE ROWS)
# # ==========================================================
# @frappe.whitelist()
# def make_stock_in(docname):

#     doc = frappe.get_doc("Repair and Service", docname)

#     if doc.inward_stock_entry:
#         return doc.inward_stock_entry

#     valid_rows = [row for row in doc.custom_repair_and_service_sku_details if row.sku_code]

#     if not valid_rows:
#         frappe.throw("Please add at least one valid SKU row")

#     se = frappe.new_doc("Stock Entry")
#     se.stock_entry_type = "Material Receipt"
#     se.company = frappe.defaults.get_user_default("Company")

#     se.set_posting_time = 1
#     se.posting_date = nowdate()

#     for row in valid_rows:

#         data = get_sku_data(row.sku_code)
#         warehouse = doc.branch or data["warehouse"]

#         se.append("items", {
#             "item_code": data["item_code"],
#             "qty": 1,
#             "batch_no": data["batch_no"],
#             "t_warehouse": warehouse,
#             "allow_zero_valuation_rate": 1,
#             "custom_sku_code": row.sku_code
#         })

#     se.insert(ignore_permissions=True)
#     se.submit()

#     doc.db_set("inward_stock_entry", se.name)
#     doc.db_set("repair_status", "In Progress")

#     return se.name


# # ==========================================================
# # STOCK OUT (MULTIPLE ROWS)
# # ==========================================================
# @frappe.whitelist()
# def make_stock_out(docname):

#     doc = frappe.get_doc("Repair and Service", docname)

#     if doc.outward_stock_entry:
#         return doc.outward_stock_entry

#     if not doc.inward_stock_entry:
#         frappe.throw("Please Receive Product First")

#     valid_rows = [row for row in doc.custom_repair_and_service_sku_details if row.sku_code]

#     if not valid_rows:
#         frappe.throw("No valid SKU rows found")

#     se = frappe.new_doc("Stock Entry")
#     se.stock_entry_type = "Material Issue"
#     se.company = frappe.defaults.get_user_default("Company")

#     se.set_posting_time = 1
#     se.posting_date = nowdate()

#     for row in valid_rows:

#         data = get_sku_data(row.sku_code)
#         warehouse = doc.branch or data["warehouse"]

#         se.append("items", {
#             "item_code": data["item_code"],
#             "qty": 1,
#             "batch_no": data["batch_no"],
#             "s_warehouse": warehouse,
#             "allow_zero_valuation_rate": 1,
#             "custom_sku_code": row.sku_code
#         })

#     se.insert(ignore_permissions=True)
#     se.submit()

#     doc.db_set("outward_stock_entry", se.name)
#     doc.db_set("repair_status", "Delivered")

#     return se.name



import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class RepairandService(Document):
    pass


@frappe.whitelist()
def get_pos_details(pos_no):

    if not pos_no:
        return {}

    pos = frappe.get_doc("POS", pos_no)

    items = []

    if hasattr(pos, "sku_details") and pos.sku_details:
        for row in pos.sku_details:
            items.append({
                "product_name": row.product or "",
                "sku_code": row.sku or "",
                "gross_weight": row.gross_weight or 0,
                "net_weight": row.net_weight or 0
            })

    return {
        "client_name": pos.client_name or "",
        "mobile_number": pos.mobile_number or "",
        "address": pos.address or "",
        "branch": pos.branch or "",
        "items": items
    }


def get_sku_data(sku_code):

    sku = frappe.get_doc("SKU", sku_code)

    return {
        "item_code": sku.product,
        "batch_no": sku.batch_no,
        "warehouse": sku.warehouse
    }


@frappe.whitelist()
def make_stock_in(docname):

    doc = frappe.get_doc("Repair and Service", docname)

    if doc.inward_stock_entry:
        return doc.inward_stock_entry

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Receipt"
    se.company = frappe.defaults.get_user_default("Company")
    se.posting_date = nowdate()
    se.set_posting_time = 1

    for row in doc.custom_repair_and_service_sku_details:
        if not row.sku_code:
            continue

        data = get_sku_data(row.sku_code)

        se.append("items", {
            "item_code": data["item_code"],
            "qty": 1,
            "batch_no": data["batch_no"],
            "t_warehouse": doc.branch or data["warehouse"]
        })

    se.insert(ignore_permissions=True)
    se.submit()

    doc.db_set("inward_stock_entry", se.name)
    doc.db_set("repair_status", "In Progress")

    return se.name


@frappe.whitelist()
def make_stock_out(docname, repair_charges=0, payment_mode=None, paid_amount=0):

    doc = frappe.get_doc("Repair and Service", docname)

    if doc.outward_stock_entry:
        return doc.outward_stock_entry

    if not doc.inward_stock_entry:
        frappe.throw("Please Receive Product First")

    if not repair_charges or not payment_mode or not paid_amount:
        frappe.throw("Payment details required")

    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type = "Material Issue"
    se.company = frappe.defaults.get_user_default("Company")
    se.posting_date = nowdate()
    se.set_posting_time = 1

    for row in doc.custom_repair_and_service_sku_details:
        if not row.sku_code:
            continue

        data = get_sku_data(row.sku_code)

        se.append("items", {
            "item_code": data["item_code"],
            "qty": 1,
            "batch_no": data["batch_no"],
            "s_warehouse": doc.branch or data["warehouse"]
        })

    se.insert(ignore_permissions=True)
    se.submit()

    doc.db_set("outward_stock_entry", se.name)
    doc.db_set("repair_status", "Delivered")

    # Save payment info
    doc.db_set("vendor_charges", repair_charges)
    doc.db_set("mode_of_payment", payment_mode)
    doc.db_set("paid_amount", paid_amount)

    return se.name