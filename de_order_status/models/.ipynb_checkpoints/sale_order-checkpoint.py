# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_status = fields.Char(string='Delivery Status', compute="_compute_delivert_status",default=' ')
    due_amount = fields.Monetary(string='Due Amount', compute='_compute_payment')
    
    

    def _compute_delivert_status(self):
        status = ''
        for line in self:
            moves = line.order_line.mapped('move_ids')
            moves_not_cancel = self.env['stock.move']
            if moves:
                status = 'Draft'
                moves_not_cancel = moves.filtered(lambda x: x.state != 'cancel')
                if all(m.state == 'cancel' for m in moves):
                    status = 'Cancelled'
            if moves_not_cancel:
                if any(m.state not in ('assigned', 'done') for m in moves_not_cancel):
                    status = 'Waiting'
                if all(m.state == 'assigned' for m in moves_not_cancel):
                    status = 'Ready'
                if any(m.state == 'done' for m in moves_not_cancel):
                    status = 'Partially Delivered'
                if all(m.state == 'done' for m in moves_not_cancel):
                    status = 'Fully Delivered'
            
            if not(status):
                status = ' '
            
            line.update({
                'delivery_status': status
            })

    def _compute_payment(self):
        payment = 0
        for line in self:
            if len(line.invoice_ids):
                payment = sum(line.invoice_ids.mapped('amount_residual'))
            else:
                payment = line.amount_total
                
            line.update({
                'due_amount': payment,
            })
           