# -*- coding: utf-8 -*-


from odoo import models, api, fields


class POSConfig(models.Model):
    """In this class the model pos.config is inherited
    to add a new boolean field in the settings of
    point of sale which is used to make enable/disable
    multiple order note in pos interface"""

    _inherit = 'pos.config'

    is_measures_guide = fields.Boolean(string='Measurement Guide',
                                 help='Allow to add measurements in POS order line',
                                 default=True)
    
    