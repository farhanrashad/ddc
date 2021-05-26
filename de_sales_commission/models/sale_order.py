# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one('res.partner', string='Agent', required=False, readonly=True,
                                         states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                         help="To address a contact in care of someone else")
    
    commission_amount = fields.Monetary(string='Commission Amount', store=True, readonly=True, compute='_amount_commission')
    
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
    
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.agent_id = self.partner_id.agent_id
        #self.commission_percentage = self.partner_id.commission_percentage

    @api.depends('order_line.commission_percentage')
    def _amount_commission(self):
        """Compute the Commission amounts of the SO"""
        total = 0
        res = super(SaleOrder, self)._amount_all()
        for line in self.order_line:
            total += (line.commission_percentage/100) * line.price_subtotal
        
        self.commission_amount = total
            
        return res
    
    def recompute_lines_agents(self):
        for line in self.order_line:
            line.update({
                'commission_percentage': self.partner_id.commission_percentage
            })

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    commission_percentage = fields.Float(string='Comm. %', readonly=True,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        #super(SaleOrderLine, self).onchange_product_id()
        self.commission_percentage = self.order_id.partner_id.commission_percentage