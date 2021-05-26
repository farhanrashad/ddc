# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    #weight = fields.Float(related='product_id.weight',string='Weight/kg',readonly=True, store=True)
    #total_weight = fields.Float('Total Weight', digits=dp.get_precision('Stock Weight'), help="Weight of the product in order line")
    production_weight = fields.Float('Weight to produce', compute='_get_production_weight', readonly=True, store=True, digits=dp.get_precision('Stock Weight'), help="Weight to be produce")
    
    @api.depends('product_id','product_qty')
    def _get_production_weight(self):
        for order in self:
            order.production_weight = order.product_id.weight * order.product_qty
    #@api.onchange('product_qty')
    #def onchange_product_uom_qty(self):
        #self.total_weight = self.product_id.weight * self.product_qty
		
	#def button_mark_done(self):
		#super(MrpProduction, self).button_mark_done()

    def post_inventory(self):
        res = super(MrpProduction, self).post_inventory()
        #for order in self:
            #moves_to_finish = order.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            #for moveline in moves_to_finish.mapped('move_line_ids'):
                #if moveline.product_id.product_tmpl_id.is_weight_uom:
                    #if moveline.location_id.usage == 'internal':
                        #moveline.product_id.product_tmpl_id.weight_available -= moveline.total_weight
                        #if not (moveline.product_id.product_tmpl_id.tracking) == 'none':
                            #moveline.lot_id.product_weight -= moveline.total_weight
                    #elif moveline.location_dest_id == 'internal':
                        #moveline.product_id.product_tmpl_id.weight_available += moveline.total_weight
                        #if not (moveline.product_id.product_tmpl_id.tracking) == 'none':
                            #moveline.lot_id.product_weight += moveline.total_weight
        return res
    
        
class MRPProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'
    
    produced_weight = fields.Float('Weight Produced', digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    @api.onchange('qty_producing')
    def _compute_produced_weight(self):
        """
        Compute the weight on change in quantity
        """
        self.produced_weight = self.qty_producing * self.product_id.weight
        
    @api.onchange('finished_lot_id')
    def onchange_finished_lot(self):
        total_qty = 0
        total_weight = 0
        for line in self.raw_workorder_line_ids:
            if line.lot_id.name == self.finished_lot_id.name:
                total_qty += line.qty_done
                total_weight += line.produced_weight
        #self.qty_producing = total_qty
        #self.produced_weight = total_weight
        
        #if self.production_id.bom_id.type == 'subcontract':
        #for mv in self.production_id.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')):
            #for mvline in mv.move_line_ids:
                #if mvline.lot_id.name == self.finished_lot_id.name:
                #total += mvline.qty_done
        
                
        
    def do_produce(self):
        """ Save the current wizard and go back to the MO. """
        res = super(MRPProductProduce, self).do_produce()
        self._product_weight_assignment()
        #for mv in self.move_raw_ids:
            #mv.total_weight = 10
        #for line in self.raw_workorder_line_ids:
            #for mv in line.move_id.move_line_ids:
                #mv.total_weight = line.produced_weight
            #for mv in line.move_id.move_line_ids:
                #mv.total_weight = line.produced_weight
        return res
    
    def continue_production(self):
        res = super(MRPProductProduce, self).continue_production()
        self._product_weight_assignment()
        #for line in self.raw_workorder_line_ids:
        
                #line.toal_weight = 111
        
        
                
        #for line in self.production_id.move_raw_ids:
            #production = self.env['mrp.product.produce.line'].search([('move_id', '=', line.id)],limit=1)
            #for mv in line.move_line_ids:
            #    mv.total_weight = production.produced_weight
            #move_lines = self.env['stock.move.line'].search([('move_id', '=', line.move_id.id)])
            #for mv in move_lines:
                #mv.write({
                #'total_weight': 10,
                #})
        return res
    
    def _product_weight_assignment(self):
        #finish weight assignment
        #for mv in self.production_id.move_finished_ids:
            #for line in mv.move_line_ids:
                #if line.lot_id == self.finished_lot_id:
                    #line.write({
                    #    'total_weight': self.produced_weight,
                    #})
        move_lines = self.env['stock.move.line'].search([('product_id', '=', self.product_id.id),('lot_id', '=', self.finished_lot_id.id),('state', '!=', 'done')])
        for line in move_lines:
            line.update({
                'total_weight':self.produced_weight
            })
        #for mv in self.production_id.move_finished_ids:
            #for line in mv.move_line_ids:
                #if line.lot_id == self.finished_lot_id:
                    #line.write({
                        #'total_weight': self.produced_weight,
                    #})
                    
        #raw material weight assignment
        if self.production_id.bom_id.type == 'normal':
            for mv in self.production_id.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')):
                for mvline in mv.move_line_ids:
                    if self.finished_lot_id and mvline.move_id.bom_line_id.bom_id.product_qty >0:
                        for lot in mvline.lot_produced_ids:
                            if lot == self.finished_lot_id:
                                if not(mvline.product_id.product_tmpl_id.uom_id.category_id.measure_type == 'weight'):
                                    mvline.write({
                                        'total_weight': self.produced_weight * (mvline.move_id.bom_line_id.product_qty/mvline.move_id.bom_line_id.bom_id.product_qty)
                                    })
                                else:
                                    mvline.write({
                                        'qty_done': self.produced_weight * (mvline.move_id.bom_line_id.product_qty/mvline.move_id.bom_line_id.bom_id.product_qty)
                                    })    
                    else:
                        if not(mvline.product_id.product_tmpl_id.uom_id.category_id.measure_type == 'weight'):
                            mvline.write({
                                'total_weight': self.produced_weight * (mvline.move_id.bom_line_id.product_qty/mvline.move_id.bom_line_id.bom_id.product_qty)
                            })
                        else:
                            mvline.write({
                                'qty_done': self.produced_weight * (mvline.move_id.bom_line_id.product_qty/mvline.move_id.bom_line_id.bom_id.product_qty)
                            })
        else:
            production_logs = self.env['mrp.production.log'].search([('product_produce_id', '=', self.id)])
            for log in production_logs:
                move_lines = self.env['stock.move.line'].search([('move_id', '=', log.move_id.id),('product_id', '=', log.product_id.id),('lot_id', '=', log.lot_id.id),('state', '!=', 'done')])
                for line in move_lines:
                    line.total_weight = log.total_weight
                
            #for mv in self.production_id.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')):
                #for line in mv.move_line_ids:
                    #if line.product_id.product_tmpl_id.is_weight_uom:
                    #move_lines = self.env['stock.move.line'].search([('product_id', '=', oline.product_id.id),('lot_id', '=', line.olot_id.id),('state', '!=', 'done')])
                    #for line in move_lines:
                        #line.write({
                            #'total_weight': self.produced_weight
                        #})
            
class MRPProductProduceLine(models.TransientModel):
    _inherit = 'mrp.product.produce.line'
    
    produced_weight = fields.Float('Weight Consumed', store=True, digits=dp.get_precision('Stock Weight'), help="Weight produced")
    
    #api.depends('raw_product_produce_id.produced_weight','product_id','lot_id','qty_done')
    api.onchange('raw_product_produce_id.produced_weight','product_id','lot_id','qty_done')
    def _calculate_produced_weight(self):
        tw = 0
        for rs in self:
            tw = 0
            tq = 0
            if rs.product_id.product_tmpl_id.is_weight_uom:
                #if self.finished_product_produce_id.subcontract_move_id:
                if rs.move_id.bom_line_id.bom_id.type == 'normal':
                    rs.produced_weight = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
                else:
                    move_lines = self.env['stock.move.line'].search([('product_id', '=', rs.product_id.id),('lot_id', '=', rs.lot_id.id),('state', '=', 'done')])
                    for line in move_lines:
                        if line.location_id.usage == 'internal':
                            tw -= line.total_weight
                            tq -= line.qty_done
                        elif line.location_dest_id.usage == 'internal':
                            tw += line.total_weight
                            tq += line.qty_done
                            
                    rs.produced_weight = rs.qty_done * (tw/tq)
            else:
                rs.produced_weight = 0
            
    @api.onchange('raw_product_produce_id.produced_weight')
    def _change_produced_qty(self):
        """
        Compute the weight on change in quantity
        """
        for rs in self:
            if not(rs.product_id.product_tmpl_id.is_weight_uom):
                rs.qty_done = rs.raw_product_produce_id.produced_weight * (rs.move_id.bom_line_id.product_qty/rs.move_id.bom_line_id.bom_id.product_qty)
                
    #@api.model
    #def write(self, values):
        #vals = {
            #'product_id': self.product_id.id,
            #'lot_id': self.lot_id.id,
            #'move_id': self.move_id.id,
            #'qty_done': self.qty_done,
            #'total_weight': self.produced_weight,
        #}
        #production_log = self.env['mrp.production.log'].write(vals)
        #move_lines = self.env['stock.move.line'].search([('product_id', '=', self.product_id.id),('lot_id', '=', self.lot_id.id),('state', '!=', 'done')])
        #for line in move_lines:
            #line.update({
                #'total_weight': produced_weight,
           # })
        #res = super(MRPProductProduceLine, self).create(values)
        #return res
                
class MrpProductionLog(models.Model):
    _name = 'mrp.production.log'
    
    product_id = fields.Many2one('product.product', 'Product Variant',)
    lot_id = fields.Many2one('stock.production.lot','lot')
    move_id = fields.Many2one('stock.move','Move')
    move_line_id = fields.Many2one('stock.move.line','Move Line')
    product_produce_id = fields.Integer('Product Produce')
    product_produce_line_id = fields.Integer('Product Produce Line')
    qty_done = fields.Float(string="quantity")
    consumed_weight = fields.Float('Consumed Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Weight consumed", oldname='total_weight')
    finished_product_id = fields.Many2one('product.product', 'Finish Product',)
    finished_lot_id = fields.Many2one('stock.production.lot','Finish Lot')
    finished_qty_done = fields.Float(string="Finish quantity")
    finished_produced_weight = fields.Float('Produced Weight', store=True, digits=dp.get_precision('Stock Weight'), help="Produced Weight")
    
    
           
    