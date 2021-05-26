# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_sale_fields_position(models.Model):
#     _name = 'de_sale_fields_position.de_sale_fields_position'
#     _description = 'de_sale_fields_position.de_sale_fields_position'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
