from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    mrp_production_plan_order_id = fields.Many2one('mrp.production.plan.order',string='Production Plan', required=False)