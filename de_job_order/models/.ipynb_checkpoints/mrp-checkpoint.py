# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    job_order_id = fields.Many2one('job.order', string='Job Order', index=True, ondelete='cascade')
    #ref_sale_id = fields.Many2one('sale.order', string='Sale Order', required=False, ondelete='cascade', index=True, copy=False, readonly=True)
    categ_id = fields.Many2one("product.category", related='product_id.product_tmpl_id.categ_id', string="Category", readonly=True)
    
    #ref_sale_id = fields.Many2one("sale.order",compute="_assign_sale_order", store=False, readonly=True,)
    ref_sale_id = fields.Many2one("sale.order",related="job_order_id.sale_id", store=True, readonly=True,)
    ref_sale_product_tmpl_id = fields.Many2one('product.template', string='Sale Product')
    
    def _assign_sale_order(self):
        #picking_id = self.id
        for line in self:
            query = """
        select distinct j.sale_id from job_order j
where j.id = %(job_order_id)s 
            """
            #self.env['stock.picking'].search([('name', '=', line.group_id.name)],limit=1).purchase_id.id
            params = {
                'job_order_id': line.job_order_id.id or 0,
                
            }
            self.env.cr.execute(query, params=params)
            #cr = self._cr
            for order in self._cr.dictfetchall():
                line.update ({
                    'ref_sale_id': order['sale_id'],
                })
                
    def post_inventory(self):
        for finish_move in self.move_finished_ids.filtered(lambda m: m.state not in ('cancel', 'done')):
            finish_move.update({
                'job_order_id': self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
            
        for finish_move_line in self.finished_move_line_ids.filtered(lambda m: m.move_id.state not in ('cancel', 'done')):
            finish_move_line.update({
                'job_order_id': self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
        for raw_move in self.move_raw_ids.filtered(lambda m: m.state not in ('cancel', 'done')):
            raw_move.update({
                'job_order_id': self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
            for raw_move_line in raw_move.move_line_ids:
                raw_move_line.update({
                    'job_order_id': self.job_order_id.id,
                    'sale_id':self.ref_sale_id.id,
                })
        res = super(MRPProduction,self).post_inventory()
        return res