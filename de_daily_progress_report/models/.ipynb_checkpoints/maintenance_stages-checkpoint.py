# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MaintenanceStages(models.Model):
    _inherit = 'maintenance.stage'

    in_progress = fields.Boolean(string="In Progress")
    is_todo = fields.Boolean(string="In Todo")
    is_done = fields.Boolean(string="In Done")
    
    
# class StockMoveLine(models.Model):
#     _inherit = 'stock.move.line'
    
#     date = fields.Date(string='Date')