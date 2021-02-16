# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from datetime import date
from datetime import time

class AllocationShift(models.Model):
    _name = 'hr.shift.allocation'
    _description = 'This table handle the data of shift allocation in attendance'
    _rec_name = 'name'

    name = fields.Char(string='Name', readonly=True)
    employee_id = fields.Many2many('hr.employee', string='Employee')
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    # day = fields.Date(string='Day')
    is_proceed = fields.Boolean(default=False)
    max_shift_day = fields.Selection([
        ('1', '1'),
        ('2', '2'),
    ], string='Max Shifts/Day', required=True, copy=False, index=True, tracking=3, default='1')

    allocation_lines = fields.One2many('hr.shift.allocation.line', 'rel_allocation')


    def unlink(self):
        raise UserError(('You Did Not Have Access Rights to Delete The Record '))


    @api.onchange('max_shift_day')
    def show_shifts(self):
        if self.max_shift_day == '1':
            self.allocation_lines.hide_field = True


    @api.onchange('date_start','date_end')
    def create_records(self):
        for line in self.allocation_lines:
            line.unlink()
        if self.date_start and self.date_end:
            delta = self.date_start - self.date_end
            total_days = abs(delta.days)
            for i in range(0, total_days + 1):
                date_after_month = self.date_start + relativedelta(days=i)
                vals = {
                    'rel_allocation': self.id,
                    'date': date_after_month,
                }
                self.env['hr.shift.allocation.line'].create(vals)
                i = i + 1

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.shift.allocation.sequence') or _('New')
        result = super(AllocationShift, self).create(vals)

        return result



    def create_management_data(self):
        self.is_proceed = True
        for employee in self.employee_id:
            line_vals = []
            for line in self.allocation_lines:
                line_vals.append((0,0, {
                    'rel_management': line.id,
                    'date': line.date,
                    'shift_one': line.shift_one_type.id,
                    'shift_two': line.shift_two_type.id,
                    'rest_day': line.rest_day,
                    'day': line.day,
                }))
            vals = {
                'employee_id': employee.id,
                'name': self.name,
                'date_start': self.date_start,
                'date_end': self.date_end,
                'management_lines': line_vals
            }
            lines = self.env['hr.shift.management'].create(vals)


class AllocationShiftLine(models.Model):
    _name = 'hr.shift.allocation.line'

    rel_allocation = fields.Many2one('hr.shift.allocation')
    date = fields.Date(string='Date')
    shift_one = fields.Boolean(string='Shift 1', default=False, readonly=True)
    shift_one_type = fields.Many2one('hr.shift', string='Shift 1 Type')
    shift_two = fields.Boolean(string='Shift 2', default=False, readonly=True)
    shift_two_type = fields.Many2one('hr.shift', string='Shift 2 Type')
    hide_field = fields.Boolean(string='Hide', default=False, readonly=True)
    rest_day = fields.Boolean(string='Rest Day')
    day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day', required=True, copy=False, index=True, tracking=3, default='monday')


    # def get_day(date_string):
    #     date = datetime.strptime(date_string, '%Y-%m-%d')
    #     print('_______________________',date)
    #     return date.day

    @api.onchange('rest_day')
    def _onchange_rest_day(self):
        for line in self:
            if line.rest_day == True:
                line.shift_one = False
                line.shift_two = False
            else:
                line.shift_one = True
                line.shift_two = True



    def unlink(self):
        if not self.env.user.has_group('de_shift_attendance.allow_allocation_deletion'):
            raise UserError(('You Did Not Have Access Rights to Delete The Record '))
        else:
            super(AllocationShiftLine,self).unlink()



