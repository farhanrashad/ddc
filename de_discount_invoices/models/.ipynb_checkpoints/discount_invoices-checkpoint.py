from odoo import models, fields, api, _


class DiscountInvoices(models.Model):
    _inherit = 'account.move'

    discount = fields.Float("Discount")
    
    total_disc = fields.Monetary(string='Total', compute='_disount_grand_tot')

    @api.depends('discount')
    def _disount_grand_tot(self):
        for order in self:
            amount_tax = 0.0
            for line in order.invoice_line_ids:
                amount_tax += ((line.tax_ids.amount)/100) * line.price_subtotal
            order.update({
                'total_disc': (order.amount_untaxed + amount_tax) - order.discount,
                'amount_total': (order.amount_untaxed + amount_tax) - order.discount,
                'amount_total_signed': (order.amount_untaxed + amount_tax) - order.discount,
                'amount_residual': (order.amount_untaxed + amount_tax) - order.discount,
                'amount_residual_signed': (order.amount_untaxed + amount_tax) - order.discount,
            })
    

   