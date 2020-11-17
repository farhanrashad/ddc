# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    warranty_count = fields.Integer(string='Warranty', compute='_compute_warranty_count')
    warranty_ids = fields.One2many('sale.warranty', 'task_id', string='Warranty')
    
    def _compute_warranty_count(self):
        wc = 0
        for line in self.order_ids.warranty_ids:
            wc += 1
        self.warranty_count = wc
        
    def action_view_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Warranty'),
            'res_model': 'sale.warranty',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
        }