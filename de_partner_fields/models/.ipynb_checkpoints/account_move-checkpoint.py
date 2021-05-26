# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    city = fields.Char(related='partner_id.city', string='City', readonly=True,store=False)
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    city = fields.Char(related='partner_id.city', string='City', readonly=True,store=False)
    team_id = fields.Many2one(related='partner_id.team_id', string='Sales Team', readonly=True,store=False)