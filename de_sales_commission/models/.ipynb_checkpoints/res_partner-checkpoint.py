# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class Partner(models.Model):
    _inherit = 'res.partner'

    agent_id = fields.Many2one('res.partner', string='Agent', required=False, help="Commission Agent")
    commission_percent = fields.Float(string='Commission Percentage')
    total_commission = fields.Monetary('Total Commission', compute='_compute_total_commission', default=0.0)

    def _compute_total_commission(self):
        """Compute total commission amount received by an agent"""
        for rs in self:
            invoices = self.env['account.move'].search([('partner_id', '=', rs.id),
                                                        ('state', 'not in', ('draft', 'cancel'))])
            if invoices:
                rs.total_commission = sum(inv.amount_total for inv in invoices)

    def action_view_care_of_invoices(self):
        """Show all invoice records having current contact as Agent"""
        self.ensure_one()
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        invoices = self.env['account.move'].search([('partner_id', '=', self.id),
                                                       ('state', 'not in', ('draft', 'cancel'))])
        action['domain'] = [
            ('id', 'in', invoices.ids),
        ]
        return action

    @api.onchange('agent_id')
    def onchange_agent_id(self):
        self.commission_percentage = self.env['ir.config_parameter'].sudo().\
            get_param('agent.commission') \
            if self.agent_id else None
