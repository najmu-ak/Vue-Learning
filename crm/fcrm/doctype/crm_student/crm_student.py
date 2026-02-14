# Copyright (c) 2024, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CRMStudent(Document):
    def validate(self):
        # Validate email format
        if self.email and not frappe.utils.validate_email_address(self.email):
            frappe.throw("Invalid email address")
        
        # Set default status if not provided
        if not self.status:
            self.status = "Active"
    
    def before_save(self):
        # Capitalize student name
        if self.student_name:
            self.student_name = self.student_name.strip().title()
