# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    wht_line_ids = fields.One2many('account.wht', 'move_id', string='Withholding Lines',copy=True, auto_join=True)
    
class InvoiceWithholdingTax(models.Model):
    _name = 'account.wht'
    _description = 'Withholding Tax'
    
    move_id = fields.Many2one('account.move',string='Account Move', track_visibility='onchange', required=True, )
    wht_type_id = fields.Many2one('account.wht.type',string='Withholding Tax Type', track_visibility='onchange', required=True, )
    base_amount = fields.Float(string='Base Amount',required=True)
    wht_amount = fields.Float(string='WHT Amount',required=True)