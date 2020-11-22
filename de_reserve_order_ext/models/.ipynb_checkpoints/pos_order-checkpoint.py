# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

class POSOrder(models.Model):
    _inherit = 'pos.order'
    
    temp_amount = fields.Text(string='Difference Amount')
    
    def button_payment_adj_action(self):
        vals = ovals = lvals = padj_vals = {}
        amount = 0
        order_id = self.env['pos.order']
        order_line_id = self.env['pos.order.line']
        for order in self:
            if order.state == 'reserved':
                for payment in order.payment_ids:
                    amount += payment.amount
                    vals = {
                        #'name': 'Reserve Order Adjustment',
                        'amount': payment.amount,
                        'pos_order_id': order_id.id,
                        'payment_method_id': payment.payment_method_id.id,
                        'session_id': order_id.session_id.id,
                        'partner_id': order_id.partner_id.id,
                    }
                order.temp_amount = order.amount_total - amount
                padj_vals = {
                    'amount': order.amount_total - amount,
                    'pos_order_id': order.id,
                    'payment_method_id': 3,
                    'session_id': order.session_id.id,
                    #'partner_id': order.partner_id.id,
                }
                #order.update({
                #    'session_id': 4,
                #})
        #pos_payment_id = self.env['pos.payment'].create(vals)
        pos_payment_id = self.env['pos.payment'].create(padj_vals)

class PosPayment(models.Model):
    """ Used to register payments made in a pos.order.

    See `payment_ids` field of pos.order model.
    The main characteristics of pos.payment can be read from
    `payment_method_id`.
    """

    _inherit = "pos.payment"
    
    @api.constrains('payment_method_id')
    def _check_payment_method_id(self):
        for payment in self:
            if not payment.pos_order_id.state == 'reserved':
                if payment.payment_method_id not in payment.session_id.config_id.payment_method_ids:
                    raise ValidationError(_('The payment method selected is not allowed in the config of the POS session.'))