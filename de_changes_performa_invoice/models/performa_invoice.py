from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    commission = fields.Char(string='Commission')
#     confirmation_date = fields.Date(string='Confirmation Date', readonly=True, index=True,
#                                     help="Date on which the sales order is confirmed.", oldname="date_confirm",
#                                     copy=False)
#     date_order = fields.Date(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.datetime.today())


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    internal_note = fields.Text(string='Note')