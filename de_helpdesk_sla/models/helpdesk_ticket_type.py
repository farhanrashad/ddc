#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket_type(models.Model):
    _name = "helpdesk.ticket.type"
    _order = "name"
    _description = "Helpdesk Ticket Type"
    
    name = fields.Char(string='Name', required=True)