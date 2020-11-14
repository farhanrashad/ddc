# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError


class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    sh_display_stock = fields.Boolean("Display Warehouse Stock")
     