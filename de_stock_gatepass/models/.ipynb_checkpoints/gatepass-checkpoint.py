# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.



import ast
from datetime import timedelta, datetime

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning
from odoo.osv.expression import OR

class Gatepass(models.Model):
    _name = 'stock.gatepass'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Gatepass'
    
    gatepass_origin = fields.Char(string='Reference')
    name = fields.Char(string='Name',  copy=False,  readonly=True, index=True, default=lambda self: _('New'))
    scheduled_date = fields.Datetime(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]})
    origin = fields.Char(string='Reference')
    driver_name = fields.Char(string='Driver')
    vehicle_no = fields.Char(string='Vehicle')
    state = fields.Selection([('draft','Draft'),
                              ('done','Done'),
                             ('cancel','Cancelled')],string = "Status", 
                             default='draft',track_visibility='onchange')
    stock_move_lines = fields.One2many('stock.move.line', 'gatepass_id', string='Move Lines', readonly=True, states={'draft': [('readonly', False)]})
    # lot = fields.Many2one('stock.production.lot', string='LOT')
    ml_count = fields.Integer(string='Move Line', compute='_compute_ml_count')
    stock_picking_id = fields.Many2one('stock.picking', string='Reference')
    stock_move_line_ids = fields.Many2many('stock.move.line')


    @api.onchange('stock_picking_id')
    def onchange_picking_id(self):
        list_ids = []
        if self.stock_picking_id:
            if self.stock_picking_id.move_ids_without_package:
                print('----------------------------self.stock_picking_id.move_ids_without_package.ids()',self.stock_picking_id.move_ids_without_package.ids)
                self.stock_move_line_ids = self.stock_picking_id.move_ids_without_package.ids
                    


#     @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.gatepass') or _('New')
        res = super(Gatepass,self).create(vals)
        return res

    def action_confirm(self):
        self.state = 'done'

    @api.depends('stock_move_lines')
    def _compute_ml_count(self):
        ml_data = self.env['stock.move.line'].sudo().read_group([('gatepass_id', 'in', self.ids)], ['gatepass_id'], ['gatepass_id'])
        mapped_data = dict([(r['gatepass_id'][0], r['gatepass_id_count']) for r in ml_data])
        for line in self:
            line.ml_count = mapped_data.get(line.id, 0)
            
    
    def action_view_move_lines1(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Move Lines'),
            'res_model': 'stock.move.line',
            'view_mode': 'tree',
            'view_id': 'de_stock_gatepass.stock_gatepass_move_line_tree_view',
            'domain': [('gatepass_id', '=', self.id)],
            'context': dict(self._context, create=False, default_gatepass_id=self.id),
        }

    
    
    
    def action_view_move_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'stock.move.line',
            'view_id': self.env.ref('de_stock_gatepass.stock_move_line_tree_view_new', False).id,
            'target': 'current',
            'domain': [('gatepass_id', '=', self.id)],
            'res_model': 'stock.move.line',
            'views': [[False, 'tree'], [False, 'form']],
        }
    
    

    line_ids = fields.One2many('stock.gatepass.line', 'gatepass_stock_id', string="Line")
    
class Gatepass(models.Model):
    _name = 'stock.gatepass.line'
    _description = 'Gatepass Lines'
    
    stock_move_line_id = fields.Many2one('stock.move.line', string="Stock Move")
    gatepass_quantity = fields.Float(string="Gatepass Quantity")
    gatepass_origin = fields.Char(string='Reference')

    gatepass_stock_id = fields.Many2one('stock.gatepass')
        
        
        
        
        
        
# stock_move_line_id many2one reference of stock.move.line
# gatepass quantity
# remaining quantity = done_qty - gatepass quantity
# related fields
# owner
# product
# done quty

