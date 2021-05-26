# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockProductionLotExt(models.Model):
    _inherit = 'stock.production.lot'

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order', store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')

    @api.onchange('partner_id')
    def _onchange_sale_order(self):
        self.partner_id = self.sale_order_id.partner_id
        same_lot = self.env['stock.production.lot'].search([('name', '=', self.name)])
        for lot in same_lot:
            lot.write({
                'sale_order_id': self.sale_order_id.id,
                'partner_id': self.partner_id.id,
            })

    # def btn_action_same_partner(self):
    #     if self.partner_id:
    #         same_lot = self.env['stock.production.lot'].search([('name', '=', self.name)])
    #         for lot in same_lot:
    #             lot.write({
    #                 # 'sale_order_id': self.sale_order_id.id,
    #                 'partner_id': self.partner_id.id,
    #             })


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order', ondelete='cascade')

    @api.onchange('lot_id')
    def _onchange_order_id(self):
        if self.lot_id:
            self.sale_order_id = self.lot_id.sale_order_id


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        if self.lot_id:
            self.owner_id = self.lot_id.partner_id

