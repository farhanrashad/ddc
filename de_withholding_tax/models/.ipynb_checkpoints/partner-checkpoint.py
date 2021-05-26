# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class Partner(models.Model):
    _inherit = 'res.partner'
    
    partner_wht_type_ids = fields.One2many('account.partner.wht', 'partner_id', string='Partner Withholding Type Ids',copy=True, auto_join=True)

class PartnerWithholdingTax(models.Model):
    _name = 'account.partner.wht'
    _description = 'Partner Withholding Tax'
    
    partner_id = fields.Many2one('res.partner',string='Partner', track_visibility='onchange', required=True, )
    wht_type_id = fields.Many2one('account.wht.type',string='Withholding Tax Type', track_visibility='onchange', required=True, )
    is_liable = fields.Boolean(string='Liable', default=True)
    exemption_number = fields.Char(string='Excemption No.')
    exempt_from = fields.Date(string='Exempt. From',required=False, )
    exempt_to = fields.Date(string='Exempt. To',required=False, )