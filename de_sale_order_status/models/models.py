# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_sale_order_status(models.Model):
#     _name = 'de_sale_order_status.de_sale_order_status'
#     _description = 'de_sale_order_status.de_sale_order_status'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
