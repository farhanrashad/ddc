# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_default_percentage = fields.Float("Default Commission Percentage", default=0, 
                                         config_parameter='sale.default_commission_percentage')
    
    calculation_type = fields.Selection(string='Calculation Type', default='net', help="Calculation type for commission",
                                        selection=[
                                            ('gross', 'Gross Amount'),
                                            ('net', 'Net Amount'),
                                            ('line', 'Line Item Total'),
                                        ], config_parameter='sale.calculation_type',)
    
    commission_default_product_id = fields.Many2one(
        'product.product',
        'Commission Product',
        domain="[('type', '=', 'service')]",
        config_parameter='sale.default_commission_product_id',
        help='Default product used for Commission')
    

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            commission_percentage=self.env['ir.config_parameter'].sudo().get_param('sale.default_commission_percentage'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sale.default_commission_percentage', self.commission_default_percentage)
        self.env['ir.config_parameter'].sudo().set_param('sale.calculation_type', self.calculation_type)



