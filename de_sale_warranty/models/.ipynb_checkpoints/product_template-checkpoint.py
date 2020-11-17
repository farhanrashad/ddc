# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging

from odoo import api, fields, models, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.tools.float_utils import float_round

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _default_period_interval(self):
        company = self.env.company
        return company.warranty_period_interval
    
    is_warranty = fields.Boolean('Allow Warranty')
    
    warranty_policy = fields.Selection([
        ('order', 'On Ordered'),
        ('delivery', 'On Delivered')], string='Warranty Policy',
        help='Ordered Warranty: Warranty starts on order confrimation.\n'
             'Delivered Warranty: Warranty starts on delivered quantity.',
        default='order', )
    
    warranty_period = fields.Selection([
        ('d', 'Day(s)'),
        ('m', 'Month(s)'),
        ('y', 'Year(s)')], string='Warranty Period',
        help='Day(s): Warranty period 1-30 days.\n'
             'Month(s): Warranty period in 1-12 months.\n'
             'Month(s): Warranty period in year(s).',
        default='d')
    
    warranty_period_interval = fields.Integer('Internval', default=_default_period_interval)

    @api.onchange('warranty_policy','type')
    def _warranty_policy_onchange(self):
        for line in self:
            if line.type == 'service':
                line.warranty_policy = 'order'