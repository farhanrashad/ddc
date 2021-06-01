# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    category_ids = fields.Many2many('res.partner.category', string='Partner Category', compute='_compute_partner_tags', store=True)
    
    def _compute_partner_tags(self):
        for tag in self:
            tag.update({
                'category_ids': [(6, 0, tag.partner_id.category_id.ids)],
            })
 