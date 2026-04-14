# app_name = "daily_reconciliation"
# app_title = "daily_reconciliation"
# app_publisher = "Sukku"
# app_description = "BOD-EOD Manager"
# app_email = "sukeshanee@gmail.com"
# app_license = "mit"

# doc_events = {
#     "POS": {                   # ✅ your actual doctype name
#         "validate": "daily_reconciliation.api.validate_bod_before_pos"
#     }
# }

# scheduler_events = {
#     "cron": {
#         "10 18 * * *": [
#             "daily_reconciliation.api.send_eod_reminder"
#         ]
#     }
# }

# doctype_js = {
#     "POS": "public/js/pos_bod_check.js"   # ✅ updated here too
# }


app_name = "daily_reconciliation"
app_title = "daily_reconciliation"
app_publisher = "Sukku"
app_description = "BOD-EOD Manager"
app_email = "sukeshanee@gmail.com"
app_license = "mit"

doc_events = {
    "POS": {
        "validate": "daily_reconciliation.api.validate_bod_before_pos"
    }
}

scheduler_events = {
    "cron": {
        "10 18 * * *": [
            "daily_reconciliation.api.send_eod_reminder"
        ]
    }
}

doctype_js = {
    "POS": "public/js/pos_bod_check.js"
}

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "daily_reconciliation",
# 		"logo": "/assets/daily_reconciliation/logo.png",
# 		"title": "daily_reconciliation",
# 		"route": "/daily_reconciliation",
# 		"has_permission": "daily_reconciliation.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/daily_reconciliation/css/daily_reconciliation.css"
# app_include_js = "/assets/daily_reconciliation/js/daily_reconciliation.js"

# include js, css files in header of web template
# web_include_css = "/assets/daily_reconciliation/css/daily_reconciliation.css"
# web_include_js = "/assets/daily_reconciliation/js/daily_reconciliation.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "daily_reconciliation/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "daily_reconciliation/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "daily_reconciliation.utils.jinja_methods",
# 	"filters": "daily_reconciliation.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "daily_reconciliation.install.before_install"
# after_install = "daily_reconciliation.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "daily_reconciliation.uninstall.before_uninstall"
# after_uninstall = "daily_reconciliation.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "daily_reconciliation.utils.before_app_install"
# after_app_install = "daily_reconciliation.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "daily_reconciliation.utils.before_app_uninstall"
# after_app_uninstall = "daily_reconciliation.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "daily_reconciliation.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"daily_reconciliation.tasks.all"
# 	],
# 	"daily": [
# 		"daily_reconciliation.tasks.daily"
# 	],
# 	"hourly": [
# 		"daily_reconciliation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"daily_reconciliation.tasks.weekly"
# 	],
# 	"monthly": [
# 		"daily_reconciliation.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "daily_reconciliation.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "daily_reconciliation.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "daily_reconciliation.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["daily_reconciliation.utils.before_request"]
# after_request = ["daily_reconciliation.utils.after_request"]

# Job Events
# ----------
# before_job = ["daily_reconciliation.utils.before_job"]
# after_job = ["daily_reconciliation.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"daily_reconciliation.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

