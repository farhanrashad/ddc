# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    repair_task_id = fields.Many2one('project.task', string="Task", help="Related Project Task")
    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket", help="Related Project Task Ticket")
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    repair_planning_line_id = fields.Many2one('project.task.planning.line', string="Planning Line", help="Related Project Planning Line")

    
    