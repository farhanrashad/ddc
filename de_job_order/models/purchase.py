# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    job_order_id = fields.Many2one('job.order', string='Job Order', index=True, ondelete='cascade')
    sale_id = fields.Many2one("sale.order",related="job_order_id.sale_id", string="Sale Order", store=True, readonly=True,)
    
    def action_view_delivery(self):
        action = self.env.ref('stock.action_picking_tree_ready')
        result = action.read()[0]
        # override the context to get rid of the default filtering on operation type
        result['context'] = {'default_partner_id': self.partner_id.id, 'default_origin': self.name, 'default_picking_type_id': self.picking_type_id.id}
        pick_ids = self.mapped('picking_ids')
        # choose the view_mode accordingly
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = pick_ids.id
        return result

    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    subcontract_move_ids = fields.One2many('stock.move', 'subcontract_order_line_id', string='Subcontract Moves', ondelete='set null', copy=False)
    
    qty_issued100 = fields.Float('Issued Quantity', copy=False, compute='_compute_qty_issued', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    weight_issued100 = fields.Float('Issued Weight', copy=False, compute='_compute_qty_issued', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    qty_issued = fields.Float(related='qty_issued100', string='Issued Qty', store=True)
    weight_issued = fields.Float(related='weight_issued100', string='Issued Weight', store=True)
    
    qty_consume100 = fields.Float('Consumed Qty', copy=False, compute='_compute_qty_consume', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    weight_consume100 = fields.Float('Consumed(Kg)', copy=False, compute='_compute_qty_consume', compute_sudo=True, store=False, digits='Product Unit of Measure', default=0.0)
    qty_consume = fields.Float(related='qty_consume100', string='Cons.Qty', store=True)
    weight_consume = fields.Float(related='weight_consume100', string='Cons.Wght', store=True)

    
    
    @api.depends('move_ids.move_orig_ids.production_id.move_raw_ids.state', 'move_ids.move_orig_ids.production_id.move_raw_ids.product_uom_qty', 'move_ids.move_orig_ids.production_id.move_raw_ids.product_uom')
    def _compute_qty_consume(self):
        #super(PurchaseOrderLine, self)._compute_qty_consume()
        for line in self:
            total = 0.0
            total_weight = 0.0
            for move in line.move_ids.move_orig_ids.production_id.move_raw_ids:
                if move.state == 'done':
                    total += move.product_uom._compute_quantity(move.product_uom_qty, move.product_uom)
                    total_weight = move.total_weight
            line.qty_consume100 = total
            line.weight_consume100 = total_weight
         
    @api.depends('subcontract_move_ids')
    def _compute_qty_issued(self):
        #self.ensure_one()
        #move_references = self.move_ids.mapped('reference')
        for line in self:
            sum_qty = 0
            sum_weight = 0
            for move in line.subcontract_move_ids:
                sum_qty += move.quantity_done
                sum_weight += move.total_weight
            line.qty_issued100 = sum_qty
            line.weight_issued100 = sum_weight

        