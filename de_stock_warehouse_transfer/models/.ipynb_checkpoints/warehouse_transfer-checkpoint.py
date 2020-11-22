# -*- coding: utf-8 -*-
from datetime import date
import time
from odoo import models, fields, api, _
from odoo import exceptions 
from odoo.exceptions import UserError, ValidationError




class StockwarehouseTransfer(models.Model):
    _name = 'stock.warehouse.transfer'
    _description = 'Warehouse Transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    
    def picking_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Picking',
            'domain': [('origin','=', self.name)],
            'target': 'current',
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
        }
    
    def action_validate(self):
            for line in self.transfer_line_ids:
                line.received_quantity = line.issue_quantity
            self.write({'state': 'validate'})

    def action_issue(self):
        picking_internal = self.env['stock.picking.type'].search([('code', '=', 'internal'),('warehouse_id','=', self.source_warehouse_id.id)], limit=1)
        vals = {
            'location_id': picking_internal.default_location_src_id.id,
            'location_dest_id': self.location_id.id,
            'origin': self.name,
            'picking_type_id': picking_internal.id,
            'state': 'waiting',
            'warehouse_transfer_id': self.id,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.transfer_line_ids:
            moves = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Internal Transfer',
                'product_uom': line.product_id.uom_id.id,
                'location_id': picking_internal.default_location_src_id.id,
                'location_dest_id': self.location_id.id,
                'product_uom_qty': line.issue_quantity,
            }
            stock_move = self.env['stock.move'].create(moves)

            move_lines = {
                'move_id': stock_move.id,
                'product_id': line.product_id.id,
                'location_id': picking_internal.default_location_src_id.id,
                'location_dest_id': self.location_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                #'product_uom_qty': line.issue_quantity,
                'qty_done': line.issue_quantity,
            }
            stock_move_line_id = self.env['stock.move.line'].create(move_lines)    
        
        picking.action_done()
        self.write({'state': 'transit'})
        for line in self.transfer_line_ids:
            line.update({
                'received_quantity': line.issue_quantity
            })
            
        
    def action_receive(self):
        p = self.env['stock.picking'].search([('warehouse_transfer_id', '=', self.id),('state', 'not in', ['done','cancel'])], limit=1)
        if p or len(p)>0:
            raise UserError(_('Please validate picking'))
            
        picking_internal = self.env['stock.picking.type'].search([('code', '=', 'internal'),('warehouse_id','=', self.dest_warehouse_id.id)], limit=1)
        vals = {
            'location_id': self.location_id.id,
            'location_dest_id': picking_internal.default_location_dest_id.id,
            'origin': self.name,
            'picking_type_id': picking_internal.id,
            'state': 'waiting',
            'warehouse_transfer_id': self.id,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.transfer_line_ids:
            moves = {
                'picking_id': picking.id,
                'reference': picking.name,
                'origin': picking.name,
                'product_id': line.product_id.id,
                'name': 'Internal Transfer',
                'product_uom': line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': picking_internal.default_location_dest_id.id,
                'product_uom_qty': line.received_quantity,
            }
            stock_move = self.env['stock.move'].create(moves)

            move_lines = {
                'move_id': stock_move.id,
                'reference': picking.name,
                'origin': picking.name,
                'product_id': line.product_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': picking_internal.default_location_dest_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                #'product_uom_qty': line.received_quantity,
                'qty_done': line.received_quantity,
            }
            stock_move_line_id = self.env['stock.move.line'].create(move_lines)    
        
        picking.action_done()
        self.write({'state': 'transfered'})
        
        
        
        
 
    
    def get_document_count(self):
        count = self.env['stock.picking'].search_count([('origin','=', self.name)])
        self.document_id = count
    
    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    document_id = fields.Integer(compute='get_document_count')
    source_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Source Warehouse', required=True,
 ondelete='cascade', readonly=True, states={'draft': [('readonly', False)]})
    location_id = fields.Many2one('stock.location', "Transit Location",
                                  required=True, readonly=True,
                                  domain="[('usage', '=', 'transit')]", 
                                  states={'draft': [('readonly', False)]})

    dest_warehouse_id = fields.Many2one(
        'stock.warehouse', 'Dest. Warehouse', required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    issue_date = fields.Datetime('Issue On', required=True, 
        default=fields.Datetime.now, readonly=True, 
        states={'draft': [('readonly', False)]},
        help="Creation Date, usually the time of the order")
    
    receive_date = fields.Datetime('Receive On', required=True, 
        default=fields.Datetime.now, readonly=True,
        states={'transit': [('readonly', False)]},
        help="Creation Date, usually the time of the order")
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('transit', 'In Transit'),
        ('transfered', 'Transfered'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    transfer_line_ids = fields.One2many('stock.warehouse.transfer.line', 'transfer_id' ,string='Transfer Line',  copy=True, states={'draft': [('readonly', False)]},)
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.warehouse.transfer') or _('New')
        res = super(StockwarehouseTransfer,self).create(vals)
        return res
    
    def unlink(self):
        for leave in self:
            if leave.state in ('transit','transfered'):
                raise UserError(_('You cannot delete an order form  which is not draft. '))
     
            return super(StockwarehouseTransfer, self).unlink()
    

class StockwarehouseTransferLine(models.Model):
    _name = 'stock.warehouse.transfer.line'
    _description = 'Stock Warehouse Transfer Line'
    
    
    product_id = fields.Many2one('product.product', 'Product', required=True,)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'UOM',required=True, domain="[('category_id', '=', product_uom_category_id)]")

    inventory_quantity = fields.Float(related='product_id.qty_available')
    issue_quantity = fields.Float(string="Transfer QTY", required=True, default=1)
    received_quantity = fields.Float(string="Received Qty", default=0, )
    
#     compute='_compute_received_qty'
    transfer_id = fields.Many2one('stock.warehouse.transfer', 'Internal Transfer', store=True)
    
    @api.constrains('issue_quantity')
    def check_quantity(self):
        for line in self:
            if line.issue_quantity > line.inventory_quantity:
                raise ValidationError('Transfer Quantity must be Less than or equal to QOH.')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_uom = self.product_id.uom_id.id
            

        
