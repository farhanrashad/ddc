# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
from datetime import date
from datetime import time

class ManagementShift(models.Model):
    _name = 'hr.shift.management'
    _description = 'This table handle the data of shift management in attendance'
    _rec_name = 'name'



    name = fields.Char(string='Name', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, readonly=True)
    date_start = fields.Date(string='Start Date', required=True, readonly=True)
    date_end = fields.Date(string='End Date', required=True, readonly=True)

    management_lines = fields.One2many('hr.shift.management.line', 'rel_management')


class ManagementShiftLine(models.Model):
    _name = 'hr.shift.management.line'

    rel_management = fields.Many2one('hr.shift.management')
    date = fields.Date(string='Date')
    shift_one = fields.Many2one('hr.shift', string='Shift 1')
    shift_two = fields.Many2one('hr.shift', string='Shift 2')
    rest_day = fields.Boolean(string='Rest Day', readonly=True)
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day', required=True, copy=False, index=True, tracking=3, default='monday')



    def unlink(self):
        if not self.env.user.has_group('de_shift_attendance.allow_management_deletion'):
            raise UserError(('You Did Not Have Access Rights to Delete The Record '))


