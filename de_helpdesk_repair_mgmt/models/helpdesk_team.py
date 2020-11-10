# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HelpdeskTicketTeam(models.Model):
    _inherit = 'helpdesk.ticket.team'
    
    project_id = fields.Many2one('project.project', string="Project", required=True, help="After Sale Service Project")
    
    