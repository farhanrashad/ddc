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
        for record in self.plan_order_lines:
            if record.production_order.state=='planned':
                raise UserError(('State of '+str(record.production_order.name)+' is already planned.\n Kindly remove it from below lines.'))
        for record in self.plan_order_lines:
            # if record.production_order.state=='planned':
            #     raise UserError(('State of '+str(record.production_order.name)+' is already planned.\n Kindly remove it from below lines.'))
            record.production_order.state = 'planned'
            record.production_order.order_set = True
        self.state = 'executed'

    name = fields.Char('Name', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    date = fields.Datetime(required=True, string="Date Time")
    note = fields.Char(string="Note")
    state = fields.Selection([('draft', 'Draft'), ('executed', 'Executed'),], default='draft', string="State")
    plan_order_lines = fields.One2many('mrp.production.plan.order.line', 'product_order')

class ProductPlanLine(models.Model):
    _name = 'mrp.production.plan.order.line'
    _description = 'Production Plan Order Line'

    # @api.onchange('production_order')
    # def onchange_production_order(self):
    #     if self.production_order:
    #         production_orders = self.env['mrp.production'].search([('name', '=', self.production_order.name)])
    #         for production_order in production_orders:
    #             production_order.update({
    #                 'order_set': True,
    #             })

    production_order = fields.Many2one('mrp.production', string='Production Order', domain=[('state', 'in', ['draft', 'confirmed']), ('order_set', '=', False)], required=True)
    product = fields.Many2one('product.product', related='production_order.product_id')
    barcode = fields.Char(related='product.barcode')
    internal_reference = fields.Char(related='product.default_code')
    quantity = fields.Float(string="Quantity", related='production_order.product_qty')
    state = fields.Selection(string='State', related='production_order.state')

    product_order = fields.Many2one('mrp.production.plan.order', required=True)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    order_set = fields.Boolean()




