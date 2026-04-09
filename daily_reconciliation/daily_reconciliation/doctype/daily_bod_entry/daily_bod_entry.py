# Copyright (c) 2026, Sukku and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class DailyBODEntry(Document):
# 	pass

import frappe
from frappe.model.document import Document
from frappe.utils import today


class DailyBODEntry(Document):

    def before_insert(self):
        self.set_today_date()
        self.check_duplicate_bod()

    def before_save(self):
        self.set_today_date()

    # ✅ Always force today's date
    def set_today_date(self):
        self.date = today()

    # ✅ Only one BOD per warehouse per day
    def check_duplicate_bod(self):
        exists = frappe.db.exists("Daily BOD Entry", {
            "date": self.date,
            "warehouse": self.warehouse,
            "name": ["!=", self.name]
        })

        if exists:
            frappe.throw(f"BOD already exists for Warehouse {self.warehouse} today")