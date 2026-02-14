# Copyright (c) 2024, Frappe Technologies and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestCRMStudent(FrappeTestCase):
    def test_student_creation(self):
        student = frappe.new_doc("CRM Student")
        student.student_name = "Test Student"
        student.email = "test@example.com"
        student.course = "Computer Science"
        student.status = "Active"
        student.insert()
        
        # Check if student is created
        self.assertTrue(frappe.db.exists("CRM Student", "Test Student"))
        
        # Clean up
        student.delete()