# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_pos_product_reference(models.Model):
#     _name = 'de_pos_product_reference.de_pos_product_reference'
#     _description = 'de_pos_product_reference.de_pos_product_reference'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
