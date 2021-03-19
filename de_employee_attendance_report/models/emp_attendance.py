from odoo import models, fields, api
import xlwt
import datetime
from odoo.exceptions import UserError


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    check_in_date = fields.Date(string="Check in", compute='compute_checkin_checkout', required=True )
    check_out_date = fields.Date(string="Check out", compute='compute_checkin_checkout', required=True )

    @api.depends('check_in','check_out')
    def compute_checkin_checkout(self):
        for rec in self:
            if rec.check_in:
                rec.check_in_date = rec.check_in.date()
            else:
                rec.check_in_date = None
            if rec.check_out:
                rec.check_out_date = rec.check_out.date()
            else:
                rec.check_out_date = None