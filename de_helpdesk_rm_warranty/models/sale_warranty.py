# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleWarranty(models.Model):
    _inherit = 'sale.warranty'
    task_id = fields.Many2one('project.task', string='Task', readonly=True)
