# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class MrpBomExt(models.Model):
    _inherit = 'mrp.bom'

    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit'), ('new', 'New')], 'BoM Type',
        default='normal', required=True)


class MrpJobOrder(models.Model):
    _name = 'mrp.job.order'
    _description = 'Job Order'

    def get_bom_lines(self):
        order_dict = []
        for rec in self:
            rec.job_order_ids.unlink()
            sale_order = self.env['sale.order'].search([('id', '=', rec.sale_id.id)])
            sale_order_lines = self.env['sale.order.line'].search([('order_id', '=', sale_order.id)])
            for sol in sale_order_lines:
                mrp_order = self.env['mrp.production'].search([('product_id', '=', sol.product_id.id)])
                for mo in mrp_order:
                    for bom in mo.bom_id.bom_line_ids:
                        ex_job_lines = self.env['mrp.job.order.material.planning'].search(
                            [('job_order_id', '=', rec.id), ('product_id', '=', bom.product_id.id)])
                        # if ex_job_lines:
                        #     qty = ex_job_lines.prod_quantity
                        #     ex_job_lines.write({
                        #         'prod_quantity': qty + bom.product_qty,
                        #     })
                        if not ex_job_lines:
                            rec.job_order_ids |= rec.job_order_ids.new({
                                'product_id': bom.product_id.id,
                                'prod_quantity': bom.product_qty,
                            })
            ex_mrp_job_order_lines = self.env['mrp.job.order.material.planning'].search([('job_order_id', '=', rec.id)])
            for ex in ex_mrp_job_order_lines:
                ex_mrp_order = self.env['mrp.production'].search([('product_id', '=', ex.product_id.id)])
                for xmo in ex_mrp_order:
                    for xbom in xmo.bom_id.bom_line_ids:
                        exx_job_lines = self.env['mrp.job.order.material.planning'].search(
                            [('job_order_id', '=', rec.id), ('product_id', '=', xbom.product_id.id)])
                        # if exx_job_lines:
                        #     xqty = exx_job_lines.prod_quantity
                        #     exx_job_lines.write({
                        #         'prod_quantity': xqty + xbom.product_qty,
                        #     })
                        if not exx_job_lines:
                            rec.job_order_ids |= rec.job_order_ids.new({
                                'product_id': xbom.product_id.id,
                                'prod_quantity': xbom.product_qty,
                            })

    # @api.multi
    # def get_bom_lines(self):
    #     for rec in self:
    #         rec.job_order_ids.unlink()
    #         order_dict = []
    #         qty_dict = []
    #         for rec in self:
    #             # rec.job_order_ids.unlink()
    #             sale_order = self.env['sale.order'].search([('id', '=', rec.sale_id.id)])
    #             print('sale_order', sale_order)
    #             sale_order_lines = self.env['sale.order.line'].search([('order_id', '=', sale_order.id)])
    #             for sol in sale_order_lines:
    #                 print('sale_order_lines', sol.product_id.name, sol.product_id.id)
    #                 mrp_order = self.env['mrp.production'].search([('product_id', '=', sol.product_id.id)])
    #                 for mo in mrp_order:
    #                     for mob in mo.bom_id.bom_line_ids:
    #                         order_dict.append(mob.product_id.id)
    #         for o in order_dict:
    #             print('order', o)
    #             ex_mrp = self.env['mrp.production'].search([('product_id', '=', o)])
    #             print('ex', ex_mrp)
    #             for ex in ex_mrp:
    #                 for e in ex.bom_id.bom_line_ids:
    #                     print('bom_line_ids', e.product_id.id)
    #                     if e.product_id.id not in order_dict:
    #                         order_dict.append(e.product_id.id)
    #         print('dict', order_dict)
    #         for res in order_dict:
    #             # rec.job_order_ids.unlink()
    #             rec.job_order_ids |= rec.job_order_ids.new({
    #                 'product_id': res,
    #                 # 'prod_quantity': res.product_qty,
    #             })

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('mrp.job.order') or 'New'
        result = super(MrpJobOrder, self).create(vals)
        return result

    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    date = fields.Date(string='Date')
    sale_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    job_order_ids = fields.One2many(comodel_name='mrp.job.order.material.planning', inverse_name='job_order_id')


class MrpJobOrderLine(models.Model):
    _name = 'mrp.job.order.material.planning'
    _description = 'Material Planning'

    def _get_stock_quantity(self):
        qty = 0.0
        for rec in self:
            stock_quant = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id)])
            for st in stock_quant:
                qty = qty + st.quantity
            rec.stock_quantity = qty

    @api.depends('tolerance_ids', 'prod_quantity')
    def _get_computed_forecast_quantity(self):
        f_qty = 0.0
        for rec in self:
            for t in rec.tolerance_ids:
                print('t', t.percentage_qty)
                f_qty = f_qty + t.percentage_qty
            rec.forecast_quantity = rec.prod_quantity + (rec.prod_quantity * f_qty/100) - rec.stock_quantity

    def mrp_process_method(self):
        for rec in self:
            result = {
                'res_model': 'order.order',
                'type': 'ir.actions.act_window',
                'context': {
                    'default_product_id': rec.product_id.id,
                    'default_ordered_qty': rec.order_quantity,
                },
                # 'res_id': emp.id,
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': self.env.ref("de_customize_ext.order_order_view_form").id,
                'target': 'new',
            }
            return result

    @api.model
    def _get_default_order_quantity(self):
        # quant = 0.0
        quant = self.forecast_quantity
        return quant

    @api.onchange('forecast_quantity')
    def onchange_preload(self):
        """ Preloads part templates if set to true"""
        if self.forecast_quantity:
            self.order_quantity = self.forecast_quantity
        else:
            self.order_quantity = 0.0

    job_order_id = fields.Many2one(comodel_name='mrp.job.order', string='Job Order Id')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    prod_quantity = fields.Float(string='Quantity')
    prod_uom = fields.Many2one(comodel_name='uom.uom', string='Unit Of Measure')
    tolerance_ids = fields.Many2many(comodel_name='mrp.job.order.tolerance', string='Tolerances')
    stock_quantity = fields.Float(string='Stock Quantity', compute='_get_stock_quantity')
    forecast_quantity = fields.Float(string='Forecast Quantity', compute='_get_computed_forecast_quantity')
    order_quantity = fields.Float(string='Order Quantity', default=_get_default_order_quantity)


class OrderOrder(models.TransientModel):
    _name = 'order.order'
    _description = 'Order Creation'

    def action_confirm(self):
        qty = 0.0
        for rec in self:
            bom_data = self.env['mrp.bom'].search([('product_tmpl_id', '=', rec.product_id.id)])
            mrp_order = self.env['mrp.production'].search([('product_id', '=', rec.product_id.id)], limit=1)
            stock_quant = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id)])
            for st in stock_quant:
                qty = qty + st.quantity
            if mrp_order:
                # print('type', bom_data.type)
                if mrp_order.bom_id.type == 'normal':
                    self.env['mrp.production'].create({
                        'product_id': rec.product_id.id,
                        'product_qty': rec.ordered_qty,
                        'date_planned_start': fields.Date.today(),
                        'product_uom_id': 1,
                        'bom_id': 11,
                    })
                    bb_prod = self.env['product.product'].search([('id', '=', rec.product_id.id)])
                    bb_prod_line = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', bb_prod.id)])
                if mrp_order.bom_id.type == 'phantom':
                    supplier_line = {
                        'product_id': rec.product_id.id,
                        'name': 'Product',
                        'product_qty': qty,
                        'price_unit': rec.product_id.list_price,
                        'order_id': rec.id,
                    }
                    b_prod = self.env['product.product'].search([('id', rec.product_id.id)])
                    b_prod_line = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', b_prod.id)], limit=1)
                    self.env['purchase.order'].create({
                        'partner_id': b_prod_line.name.id,
                        'date_order': fields.Date.today(),
                        'order_line': [(0, 0, supplier_line)],
                    })

    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    ordered_qty = fields.Float(string='Quantity')
