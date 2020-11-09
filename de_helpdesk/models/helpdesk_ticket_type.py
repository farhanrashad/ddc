from odoo import fields, models


class HelpdeskTicketType(models.Model):

    _name = 'helpdesk.ticket.type'
    _description = 'Helpdesk Ticket Type'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )
