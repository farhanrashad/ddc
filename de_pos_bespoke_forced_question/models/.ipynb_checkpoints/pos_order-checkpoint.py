# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

class POSOrder(models.Model):
    _inherit = 'pos.order'
    
    is_bespoke_ordered = fields.Boolean(string='Bespoke Ordered', )

    #@api.model
    def button_bespoke_order(self):
        query = ''
        question_ids = []
        vals = {}
        pos_question_id = self.env['pos.order.line.questions']
        for line in self.lines:
            if line.product_id.product_tmpl_id.is_bespoke:
                #query = 'select pg.forced_question_group_id as group_id, gr.pos_forced_question_id as question_id, pg.product_template_id as product_tmpl_id from forced_question_group_product_template_rel pg join forced_question_group_pos_forced_question_rel gr on pg.forced_question_group_id = gr.forced_question_group_id where pg.product_template_id = %(pid)s' 
                #params = {'pid': line.product_id.product_tmpl_id.id or 0,}
                #self.env.cr.execute(query, params=params)
                #for question in self._cr.dictfetchall():
                bvals = {
                    'state':'draft',
                    'pos_order_line_id':line.id,
                }
                bespoke_id = self.env['pos.bespoke.order'].create(bvals)
                for group in line.product_id.product_tmpl_id.question_group_ids:
                    vals = {
                        'pos_order_line_id':line.id,
                        'question_group_id': group.id,
                        'bespoke_order_id': bespoke_id.id,
                    }
                    pos_question_id = self.env['pos.order.line.questions'].create(vals)
                
                
        #self.is_bespoke_ordered = True

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    #pos_line_questions_ids = fields.One2many('pos.order.line.questions', 'pos_order_line_id' ,string='Pos Line Questions',  copy=True, states={'draft': [('readonly', False)]},)
    
class PosOrderLineQuestions(models.Model):
    _name = 'pos.order.line.questions'
    _description = 'POS Order line Questions'
    
    
    pos_order_line_id = fields.Many2one('pos.order.line', 'POS Order Line', required=True)
    name = fields.Many2one('pos.order', related='pos_order_line_id.order_id', string='POS Order', )
    question_group_id = fields.Many2one('forced.question.group', 'Question Group', required=True)
    question_id = fields.Many2one('pos.forced.question', 'Question', required=False )

    bespoke_order_id = fields.Many2one('pos.bespoke.order', string='Bespoke Order', index=True, ondelete='cascade')

