import frappe
from frappe.model.document import Document
from frappe.utils import today


class DailyEODEntry(Document):

    def before_insert(self):
        self.set_today_date()
        self.check_duplicate_eod()

    def before_save(self):
        self.set_today_date()
        self.get_bod_values()
        self.calculate_variance()

    def before_submit(self):
        self.validate_variance()
        self.validate_approval()

    # ✅ Always force today's date
    def set_today_date(self):
        self.date = today()

    # ✅ Only one EOD per warehouse per day
    def check_duplicate_eod(self):
        exists = frappe.db.exists("Daily EOD Entry", {
            "date": self.date,
            "warehouse": self.warehouse,
            "name": ["!=", self.name]
        })

        if exists:
            frappe.throw(f"EOD already exists for Warehouse {self.warehouse} today")

    # ✅ Fetch BOD
    def get_bod_values(self):
        bod = frappe.db.get_value(
            "Daily BOD Entry",
            {
                "date": self.date,
                "warehouse": self.warehouse
            },
            [
                "opening_stock_count",
                "opening_main_cash",
                "opening_petty_cash",
                "opening_walkin_count"
            ],
            as_dict=True
        )

        if not bod:
            frappe.throw("BOD Entry not found for this Warehouse")

        self.opening_stock = bod.opening_stock_count or 0
        self.opening_main_cash = bod.opening_main_cash or 0
        self.opening_petty_cash = bod.opening_petty_cash or 0
        self.opening_walkin = bod.opening_walkin_count or 0

    # ✅ Calculate Variance
    def calculate_variance(self):

        self.stock_variance = (self.closing_stock_count or 0) - self.opening_stock
        self.main_cash_variance = (self.closing_main_cash or 0) - self.opening_main_cash
        self.petty_cash_variance = (self.closing_petty_cash or 0) - self.opening_petty_cash
        self.walk_in_variance = (self.closing_walk_in_count or 0) - self.opening_walkin

    # ✅ Block submit if mismatch
    def validate_variance(self):

        if (
            self.stock_variance != 0 or
            self.main_cash_variance != 0 or
            self.petty_cash_variance != 0 or
            self.walk_in_variance != 0
        ):
            if not self.allow_override:
                frappe.throw("Variance exists! Cannot submit without override")

    # ✅ Approval required if override
    def validate_approval(self):
        if self.allow_override and not self.approved_by:
            frappe.throw("Approved By is required when override is enabled")