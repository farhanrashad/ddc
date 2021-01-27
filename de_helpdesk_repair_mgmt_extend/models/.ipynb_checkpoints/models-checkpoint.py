# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskExtendInherit(models.Model):
    _inherit = 'helpdesk.ticket.team'

    technician_ids = fields.Many2many('res.users','helpdesk_ticket_teams_res_users_rel', string='Technician')


class HelpdeskExtends(models.Model):
    _inherit = 'helpdesk.ticket'
    
    team = fields.Many2many(related='team_id.technician_ids', string='rel', invisible=True)
    
    technician_id = fields.Many2one('res.users',string='Technician', domain="[('id','in',team)]")