from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
from datetime import date
import calendar

class EmployeeAttandanceWizard(models.Model):
    _name = "employee.attendance.wizard"
    _description = "Employee Wizard"

    date_from=fields.Date(string="Date From", default=date.today())
    date_to=fields.Date(string="Date To", default=date.today())
    employee=fields.Many2many('hr.employee', string="Employee")
    
    def action_report_gen(self):
        data = {}
        data['form'] = self.read(['employee', 'date_from', 'date_to'])[0]
        return self.env.ref('de_employee_attendance_report.employee_attendance_report').report_action(self, data=data, config=False)