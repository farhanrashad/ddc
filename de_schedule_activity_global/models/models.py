from odoo import models, fields, api
from datetime import datetime


class ScheduleActivity(models.Model):
    _inherit = 'mail.activity'

    current_date = fields.Date('Current Date', compute='get_date')

    @api.depends('current_date')
    def get_date(self):
        self.current_date = datetime.today().date()
