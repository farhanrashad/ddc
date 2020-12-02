from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductionPlan(models.Model):
    _name = 'mrp.production.plan.order'
    _description = 'Production Plan Order'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('plan.production.sequence')
        result = super(ProductionPlan, self).create(vals)
        return result

    def action_execute_plan(self):
        for record in self.production_ids:
            if record.state=='planned':
                raise UserError(('State of '+str(record.production_order.name)+' is already planned.\n Kindly remove it from below lines.'))
        for record in self.production_ids:
            record.state = 'planned'
        self.state = 'executed'

    name = fields.Char('Name', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    date = fields.Datetime(required=True, string="Date Time", readonly=True, states={'draft': [('readonly', False)]})
    note = fields.Char(string="Note")
    state = fields.Selection([('draft', 'Draft'), ('executed', 'Executed'),], default='draft', string="State")
    
    production_ids = fields.One2many('mrp.production', 'mrp_production_plan_order_id', string='Productions', readonly=True, states={'draft': [('readonly', False)]})






