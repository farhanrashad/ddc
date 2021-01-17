# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_bespoke = fields.Boolean(string='Allowed Bespoke',
                                 help="Check if the product should be bespoke order")
    
    is_open_bespoke_component_service = fields.Boolean(related='pos_categ_id.is_open_bespoke_component_service', string='Open Bespoke Component Service', help="Create a product as services for reference component")
    
    bespoke_component_product_template_id = fields.Many2one('product.template',string='Bespoke Component')
    
    @api.returns('self', lambda value: value.id)
    def open_bespoke_service_action(self, default=None):
        # TDE FIXME: should probably be copy_data
        self.ensure_one()
        if default is None:
            default = {}
        bespoke_service_id = super(ProductTemplate, self).copy(default=default)
        self.update({
            'bespoke_component_product_template_id': bespoke_service_id.id,
        })
        bespoke_service_id.update({
            'categ_id': self.pos_categ_id.bespoke_category_id.id,
            'pos_categ_id': self.pos_categ_id.bespoke_pos_categ_id.id,
            'is_bespoke': False,
            'type': 'service',
            'name': self.name,
        })
        return bespoke_service_id
    
class ProductCategory(models.Model):
    _inherit = 'pos.category'
    
    is_open_bespoke_component_service = fields.Boolean(string='Open Bespoke Component Service',
                                                       help="Create a product as services for reference component")
    bespoke_category_id = fields.Many2one('product.category', string='Component Inventory Category')
    bespoke_pos_categ_id = fields.Many2one('pos.category', string='Component POS Category')


