# -*- coding: utf-8 -*-
from datetime import date
import time
from odoo import models, fields, api, _
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError


class BespokeOrder(models.Model):
    _name = 'pos.bespoke.order'
    _description = 'POS Bespoke Order'
    
    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    date_ordered = fields.Datetime('Order On', required=True, 
                                   default=fields.Datetime.now, readonly=True, 
                                   states={'draft': [('readonly', False)]},
                                   help="Order Date, usually the time of the order")
    delivery_date = fields.Datetime('Delivery On', required=False, 
                                   default=fields.Datetime.now, readonly=True, 
                                   states={'draft': [('readonly', False)]},
                                   help="Delivery Date, usually the time of the order")
    
    state = fields.Selection([
        ('draft', 'New'),
        ('ready', 'Ready'),
        ('confirmed', 'Confirm'),
        ('wait', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id, readonly=True, states={'draft': [('readonly', False)], 'ready': [('readonly', False)], 'confirmed': [('readonly', False)]})
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")

    
    pos_order_line_id = fields.Many2one('pos.order.line', 'POS Order Line', )
    pos_order_id = fields.Many2one('pos.order', related='pos_order_line_id.order_id', string='POS Order', )
    partner_id = fields.Many2one('res.partner', related='pos_order_id.partner_id', string='Customer', )

    
    bespoke_product_id = fields.Many2one('product.product', 'Product', readonly=True, states={'draft': [('readonly', False)], 'ready': [('readonly', False)], 'confirmed': [('readonly', False)]})
    
    pos_product_id = fields.Many2one('product.product', related='pos_order_line_id.product_id')
    product_qty = fields.Float(string='Quantity', related='pos_order_line_id.qty', digits='Product Unit of Measure', )
    price_unit = fields.Float(string='Unit Price', related='pos_order_line_id.price_unit')
    total_amount = fields.Float(compute='_compute_amount', string='Total',readonly=True)
    paid_amount = fields.Float(compute='_compute_balance_amount', string='Paid Amount',readonly=True)
    due_amount = fields.Float(compute='_compute_balance_amount', string='Due Amount',readonly=True)
    
    bespoke_bom_id = fields.Many2one('mrp.bom', 'BOM', readonly=True, states={'draft': [('readonly', False)], 'ready': [('readonly', False)], 'confirmed': [('readonly', False)]})
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', readonly=True, states={'draft': [('readonly', False)], 'ready': [('readonly', False)], 'confirmed': [('readonly', False)]})
    
    polq_ids = fields.One2many('pos.order.line.questions', 'bespoke_order_id', string='Questions')
    polq_count = fields.Integer(string='Questions', compute='_compute_questions_count')
    
    picking_ids = fields.One2many('stock.picking', 'bespoke_order_id', string='Picking')
    picking_count = fields.Integer(string='Picking', compute='_compute_picking_count')
    
    production_ids = fields.One2many('mrp.production', 'bespoke_order_id', string='Production')
    production_count = fields.Integer(string='Production', compute='_compute_production_count')
    
    invoice_ids = fields.One2many('account.move', 'bespoke_order_id', string='Invoice')
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoices_count')
    
    total_payments_amount = fields.Float(compute='_compute_total_payments_amount', string='Total Payments Amount')
    
    test1 = fields.Char('test')
    
    @api.depends('pos_order_line_id')
    def _compute_qty_price(self):
        for line in self:
            line.update({
                'product_qty': line.pos_order_line_id.qty,
                'price_unit': line.pos_order_line_id.price_unit,
            })
            
    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.update({
                'total_amount': line.pos_order_line_id.price_subtotal_incl,
            })

    @api.depends('pos_order_id.payment_ids.amount')
    def _compute_balance_amount(self):
        amt = 0
        pos_payment_ids = self.env['pos.payment'].search([('pos_order_id','=',self.pos_order_id.id)])
        for line in pos_payment_ids.filtered(lambda r: r.payment_method_id.is_cash_count == True ):
            amt += line.amount
        self.paid_amount = amt
        self.due_amount = self.total_amount - self.paid_amount
        
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('pos.bespoke.order') or _('New')
        res = super(BespokeOrder,self).create(vals)
        return res
    
    def button_mark_to_do(self):
        self.write({'state': 'ready'})
        
    def button_confirm(self):
        s = []
        pq_lines = self.env['pos.order.line.questions']
        question = self.env['pos.forced.question']
        c = 0
        prod_long_name = prod_short_name = ''
        for line in self:
            c = 0
            s = line.pos_order_line_id.forced_questions.split('|')
            pq_lines = self.env['pos.order.line.questions'].search([('pos_order_line_id','=',line.pos_order_line_id.id)])
            
            for q in pq_lines:
                question = self.env['pos.forced.question'].search([('name','=',s[c])],limit=1)
                q.update({
                    'question_id':question.id,
                })
                c+=1
                if question.product_property_is_short:
                    prod_short_name += question.product_property_line_id.name + '|'
                if question.product_property_is_long:
                    prod_long_name += question.product_property_line_id.description + ' '
                    
            vals = {
                'name':prod_long_name,
                'default_code': prod_short_name,
                'sale_ok':True,
                'purchase_ok':False,
                'type':'product',
                'categ_id':1,
            }
            line.test1 = prod_short_name + ' / ' + prod_long_name
            product_tmpl_id = self.env['product.template'].create(vals)
            bom_id = self.env['mrp.bom'].create({
                'product_tmpl_id': product_tmpl_id.id,
                'product_qty':1,
                'code':self.name,
                'type':'normal',
            })
            product_id = self.env['product.product'].search([('product_tmpl_id','=',product_tmpl_id.id)],limit=1)
            line.update({
                'bespoke_product_id':product_id.id,
                'bespoke_bom_id':bom_id.id,
            })
        for pline in self.pos_order_id.lines:
            if not pline.product_id.type == 'service':
                if not pline.product_id.product_tmpl_id.is_bespoke:
                    bom_line_id = self.env['bom_line_id'].create({
                        'bom_id': bom_id.id,
                        'product_id': pline.product_id.id,
                        'product_qty': (pline.qty/self.product_qty),
                        'product_uom_id': pline.product_id.uom_id.id,
                    })
        
            
        self.write({
            'bespoke_product_id':product_id.id,
            'state': 'confirmed',
        })
    def button_create_delivery(self):
        #Create Delivery
        if not self.warehouse_id:
            raise exceptions.UserError('Please select warehouse for delivery.')
        
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'outgoing'),('warehouse_id','=', self.warehouse_id.id)], limit=1)
        customer_location_id = self.env['stock.location'].search([('usage', '=', 'customer')], limit=1)

        vals = {
            'partner_id': self.partner_id.id,
            'location_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': customer_location_id.id,
            'origin': self.name,
            'bespoke_order_id': self.id,
            'picking_type_id': picking_type_id.id,
            'state': 'draft',
        }
        picking = self.env['stock.picking'].create(vals)
        for pline in self:
            moves = {
                'picking_id': picking.id,
                'product_id': pline.bespoke_product_id.id,
                'name': pline.bespoke_product_id.name,
                'product_uom': pline.bespoke_product_id.uom_id.id,
                'location_id': picking_type_id.default_location_src_id.id,
                'location_dest_id': customer_location_id.id,
                'product_uom_qty': pline.product_qty,
            }
            stock_move = self.env['stock.move'].create(moves)
    
    def button_create_production(self):
        #Create Production
        if not self.warehouse_id:
            raise exceptions.UserError('Please select warehouse for Production.')
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'mrp_operation'),('warehouse_id','=', self.warehouse_id.id)], limit=1)
        vals = {
            'product_id': self.bespoke_product_id.id,
            'product_uom_id':self.bespoke_product_id.uom_id.id,
            'product_qty': self.product_qty,
            'bom_id': self.bespoke_bom_id.id,
            'picking_type_id': picking_type_id.id,
            'location_src_id': picking_type_id.default_location_src_id.id,
            'location_dest_id': picking_type_id.default_location_dest_id.id,
            'origin': self.name,
            'bespoke_order_id': self.id,
            'state': 'draft',
        }
        production_id = self.env['mrp.production'].create(vals)
        self.write({'state': 'wait'})
        
    def button_cancel(self):
        self.write({'state': 'cancel'})
        
    @api.depends('polq_ids')
    def _compute_questions_count(self):
        question_data = self.env['pos.order.line.questions'].sudo().read_group([('bespoke_order_id', 'in', self.ids)], ['bespoke_order_id'], ['bespoke_order_id'])
        mapped_data = dict([(r['bespoke_order_id'][0], r['bespoke_order_id_count']) for r in question_data])
        for line in self:
            line.polq_count = mapped_data.get(line.id, 0)

    def action_view_questions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Questions'),
            'res_model': 'pos.order.line.questions',
            'view_mode': 'tree,form',
            'domain': [('bespoke_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_bespoke_order_id=self.id),
        }
    
    @api.depends('picking_ids')
    def _compute_picking_count(self):
        picking_data = self.env['stock.picking'].sudo().read_group([('bespoke_order_id', 'in', self.ids)], ['bespoke_order_id'], ['bespoke_order_id'])
        mapped_data = dict([(r['bespoke_order_id'][0], r['bespoke_order_id_count']) for r in picking_data])
        for line in self:
            line.picking_count = mapped_data.get(line.id, 0)
            #line.picking_count = 0

    def action_view_pickings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pickings'),
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('bespoke_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_bespoke_order_id=self.id),
        }
    
    @api.depends('production_ids')
    def _compute_production_count(self):
        production_data = self.env['mrp.production'].sudo().read_group([('bespoke_order_id', 'in', self.ids)], ['bespoke_order_id'], ['bespoke_order_id'])
        mapped_data = dict([(r['bespoke_order_id'][0], r['bespoke_order_id_count']) for r in production_data])
        for line in self:
            line.production_count = mapped_data.get(line.id, 0)

    def action_view_production(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Production'),
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
            'domain': [('bespoke_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_bespoke_order_id=self.id),
        }
    
    
    @api.depends('invoice_ids')
    def _compute_invoices_count(self):
        invoice_data = self.env['account.move'].sudo().read_group([('bespoke_order_id', 'in', self.ids)], ['bespoke_order_id'], ['bespoke_order_id'])
        mapped_data = dict([(r['bespoke_order_id'][0], r['bespoke_order_id_count']) for r in invoice_data])
        for line in self:
            line.invoice_count = mapped_data.get(line.id, 0)

    def action_view_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('bespoke_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_bespoke_order_id=self.id),
        }

    @api.depends('pos_order_id.payment_ids.amount')
    def _compute_total_payments_amount(self):
        for line in self:
            line.total_payments_amount = sum(line.pos_order_id.mapped('payment_ids.amount'))
            
    def action_show_payments_list(self):
        return {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.payment',
            'view_mode': 'tree,form',
            'domain': [('pos_order_id', '=', self.pos_order_id.id)],
            'context': {'search_default_group_by_payment_method': 1}
        }
    
    