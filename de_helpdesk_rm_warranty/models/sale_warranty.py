# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleWarranty(models.Model):
    _inherit = 'sale.warranty'
    task_id = fields.Many2one('project.task', string='Task', readonly=True)

    repair_planning_ids = fields.One2many('project.task.planning.line', 'warranty_id', string='Warranty', 
                                         )
    #domain="[('is_diagnosys','=',True),('active','=',True),('project_id','=',project_id)]")
