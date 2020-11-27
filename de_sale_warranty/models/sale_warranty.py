# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SaleWarranty(models.Model):
    _name = 'sale.warranty'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Sale Warranty'
    _order = 'id desc'
    
    name = fields.Char(string='Name',  copy=False,  readonly=True, index=True, default=lambda self: _('New'))
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    product_id = fields.Many2one('product.product',string='Product', track_visibility='onchange', required=True, readonly=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    barcode = fields.Char(related='product_id.barcode',string='Barcode')
    tracking = fields.Selection(related='product_id.tracking', string='Tracking')
    origin = fields.Char(string='Reference')
    #sno = fields.Char(string='Serial No',track_visibility='onchange', readonly=True,states={'draft': [('readonly', False)]},)
    lot_id = fields.Many2one('stock.production.lot',domain="[('product_id', '=', product_id)]",states={'draft': [('readonly', False)]},string='Serial No.')
    partner_id = fields.Many2one('res.partner',string='Customer', required=True, track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    sale_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    warranty_type_id = fields.Many2one('sale.warranty.type',string='Warranty Type', required=True, help="Type or Mode of the warranty")
    picking_id = fields.Many2one('stock.picking', string='Delivery Order', readonly=True)
    invoice_id = fields.Many2one('account.invoice',string='Invoice',readonly=True)
    purchase_date = fields.Date(string='Date of Purchase',required=False, readonly=True, states={'draft': [('readonly', False)]})
    warranty_start_date = fields.Date(string='Warranty Start Date',track_visibility='onchange',required=True, readonly=True, states={'draft': [('readonly', False)]})
    warranty_end_date = fields.Date(string='Warranty End Date',track_visibility='onchange',required=False, readonly=True, states={'draft': [('readonly', False)]})
    
    state = fields.Selection([('draft','Draft'),
                              ('inwarranty','In Warranty'),
                              ('toexpire','To Expire'),
                              ('expired','Expired'),
                             ('cancel','Cancelled')],string = "Status", default='draft',track_visibility='onchange')
    
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    
    
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.warranty_start_date = datetime.date.today()
        if self.product_id.warranty_period == 'y':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=(self.product_id.warranty_period_interval*365))
        elif self.product_id.warranty_period == 'm':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=(self.product_id.warranty_period_interval*30))
        elif self.product_id.warranty_period == 'd':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=self.product_id.warranty_period_interval)
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.warranty') or _('New')
        res = super(SaleWarranty,self).create(vals)
        return res
    
        
    def start_warranty(self):
        warranty = self.env['sale.warranty'].search([
            ('partner_id','=',self.partner_id.id),
            ('product_id','=',self.product_id.id),
            ('lot_id','=', self.lot_id.id),
            ('state','=','inwarranty'),
        ])
        if len(warranty):
            raise UserError(_('Product is already in-warrany.'))
        else:
            self.state = 'inwarranty'
    
    def force_expire_warranty(self):
        self.state = 'expired'
        
    def unlink(self):
        for rs in self:
            if rs.state not in ('draft'):
                raise UserError(_('You can not delete a running warranty.'))
        return super(SaleWarranty, self).unlink()
    
    @api.model
    def cron_warranty_expire(self):
        date_eval =  datetime.now()+timedelta(days=30)
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty = self.env['sale.warranty'].search([('warranty_end_date','<=',date_eval_str),
                                                                ('state','=','inwarranty')])
        for wty in warranty:                        
            wty.state = 'toexpire'
     
    @api.model
    def cron_warranty_expired(self):
        date_eval =  datetime.now()
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty = self.env['sales.warranty'].search([('warranty_end_date','<=',date_eval_str)])
        for wty in warranty:                        
            wty.state = 'expired'    