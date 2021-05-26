# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import chain

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.misc import get_lang

from odoo.addons import decimal_precision as dp

class SalesCommission(models.Model):
    _name = 'sale.commission'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Sale Commission"
    _order = 'doc_date desc, id desc'
    
    @api.model
    def _default_product_id(self):
        product_id = self.env['ir.config_parameter'].sudo().get_param('sale.default_commission_product_id')
        return self.env['product.product'].browse(int(product_id)).exists()
    

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, state={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    currency_id = fields.Many2one("res.currency", string="Currency", required=True, readonly=True, states={'draft': [('readonly', False)]}, )
    
    agent_id = fields.Many2one('res.partner', string='Agent', required=True, help="Commission Agent", readonly=True, states={'draft': [('readonly', False)]}, )
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)
    
    doc_date = fields.Datetime(string='Date', required=True, index=True, copy=False, default=fields.Datetime.now, readonly=True, states={'draft': [('readonly', False)]}, )
    product_id = fields.Many2one('product.product', required=True, string='Product', domain=[('type', '=', 'service')],
                                 readonly=True, states={'draft': [('readonly', False)]}, default=_default_product_id)
    
    commission_amount = fields.Float(string='Comm. Amount',required=True, readonly=True, states={'draft': [('readonly', False)]}, )
    sale_id = fields.Many2one('sale.order', 'Sale Order',required=False, domain="[('state', 'in', ['sale','done'])]", readonly=True, states={'draft': [('readonly', False)]}, )
    sale_amount = fields.Monetary(string='Total Sale', related='sale_id.amount_total', store=True, readonly=True, )
    is_invoiced = fields.Boolean('Is Invoiced', default=False, readonly=True, )
    invoice_id = fields.Many2one('account.move', 'Invoice',required=False,  readonly=True, )
    date_invoiced = fields.Datetime(string='Date Invoiced', required=False, readonly=True)
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('sale.commission') 
        values['name'] = seq
        res = super(SalesCommission,self).create(values)
        return res
    
    def action_confirm(self):
        self.state = 'posted'
        
    def action_create_invoice(self):
        self.state = 'paid'
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def unlink(self):
        for rs in self:
            if rs.state not in ('draft'):
                raise UserError(_('You can not delete a posted document.'))
        return super(SalesCommission, self).unlink()
    