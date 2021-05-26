# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class WithholdingTaxGroup(models.Model):
    _name = 'account.wht.group'
    _description = 'Withholding Tax Group'
    
    name = fields.Char(string='Name',  copy=False,  index=True, required=True)
    
class WithholdingTax(models.Model):
    _name = 'account.wht.type'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Withholding Tax'
    _order = 'id desc'
    
    code = fields.Char(string='Code',required=True)
    name = fields.Char(string='Name',  copy=False,  index=True, required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    wht_type = fields.Selection(string='WHT Scope', required=True,  help="Scope of withholding tax i.e Vendor Payment or Customer Payment", default="out_payment", selection=[('out_payment', 'WHT on Outgoing Payment'), ('in_payment', 'WHT on Incoming Payment')])
    active = fields.Boolean(string='Active', default=True)
    wht_rate = fields.Float(string='WHT Rate', required=True, default='0')
    wht_group_id = fields.Many2one('account.wht.group',string='Withholding Tax Group', track_visibility='onchange', required=True, )
    description = fields.Char(string='Label')
    account_id = fields.Many2one('account.account',string='Account', track_visibility='onchange', required=True, )
    base_amount = fields.Selection(string='Base Amount', required=True,  help="Base amount for tax calcualtion", selection=[('net', 'Net Amount'), ('gross', 'Gross Amount'),('tax', 'Tax Amount')])
    
    manual_base_amount = fields.Boolean(string='Base Amount Manual', default=True)
    manual_tax_amount = fields.Boolean(string='Active', default=True)
    is_certification_number = fields.Boolean(string='Certification Number', default=True)