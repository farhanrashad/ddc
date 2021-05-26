# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp
class Picking(models.Model):
    _inherit = 'stock.picking'
    
#     job_order_id = fields.Many2one('job.order', related='purchase_id.job_order_id', string='Job Order', readonly=True, store=True)
    job_order_id = fields.Many2one("job.order", compute="_assign_sale_order", store=False, string="Job Order", readonly=True, required=False)
    ref_sale_id = fields.Many2one("sale.order",compute="_assign_sale_order", store=False, readonly=True,)
    job_order_new = fields.Many2one("job.order",string="Job Order",readonly=True,required=False)
    ref_sale_new = fields.Many2one("sale.order", readonly=True,string="Ref Sale",related="job_order_new.sale_id")
    
    def _assign_sale_order2(self):
        #move_line_obj = self.env['stock.move.line'].search[()]
        for line in self:
            line.update({
                'ref_sale_id': line.sale_id.id
            })
        
    def _assign_sale_order(self):
        #picking_id = self.id
        for line in self:
            picking = self.env['stock.picking'].search([('name', '=', line.group_id.name)],limit=1)
            query = """
            select max(a.job_order_id) as job_order_id,max(a.sale_id) as sale_id from (
select p.job_order_id,p.sale_id from purchase_order p
where p.id = %(purchase_id)s
union all
select j.id as job_order_id, s.id as sale_id from sale_order s
left join job_order j on j.sale_id = s.id
where s.id = %(sale_id)s
) a
            """
            params = {
                'purchase_id': line.purchase_id.id or 0,
                'sale_id': line.sale_id.id or 0,
            }
            self.env.cr.execute(query, params=params)
            #cr = self._cr
            
            for order in self._cr.dictfetchall():
                line.update ({
                    'job_order_id': order['job_order_id'] or picking.job_order_id.id,
                    'job_order_new': order['job_order_id'] or picking.job_order_id.id,
                    'ref_sale_id': order['sale_id'] or picking.ref_sale_id.id,
                    'ref_sale_new': order['sale_id'] or picking.ref_sale_id.id,
                })
        
    def _assign_sale_order1(self):
        select = 0
        from_clause, where_clause, where_clause_params = ''
        move_line_obj = self.env['stock.move.line']
        for line in self:
            if len(line.move_line_ids):
                domain = [('product_id', '=', line.product_id.id),
                          ('state', '=', 'done'),
                          
                          ]

                where_query = move_line_obj._where_calc(domain)
                move_line_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(total_weight) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.total_weight = self.env.cr.fetchone()[0] or 0.0
            
    def button_validate(self):
        for movewp in self.move_ids_without_package:
            movewp.update({
                'job_order_id':self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
            for line in movewp.move_line_ids:
                line.update({
                    'job_order_id':self.job_order_id.id,
                    'sale_id':self.ref_sale_id.id,
                })
        for move in self.move_lines:
            move.update({
                'job_order_id':self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
            for line in move.move_line_ids:
                line.update({
                    'job_order_id':self.job_order_id.id,
                    'sale_id':self.ref_sale_id.id,
                })
        for mline in self.move_line_ids:
            mline.update({
                'job_order_id':self.job_order_id.id,
                'sale_id':self.ref_sale_id.id,
            })
        res = super(Picking,self).button_validate()
        return res