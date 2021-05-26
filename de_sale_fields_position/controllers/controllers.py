# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleFieldsPosition(http.Controller):
#     @http.route('/de_sale_fields_position/de_sale_fields_position/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_fields_position/de_sale_fields_position/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_fields_position.listing', {
#             'root': '/de_sale_fields_position/de_sale_fields_position',
#             'objects': http.request.env['de_sale_fields_position.de_sale_fields_position'].search([]),
#         })

#     @http.route('/de_sale_fields_position/de_sale_fields_position/objects/<model("de_sale_fields_position.de_sale_fields_position"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_fields_position.object', {
#             'object': obj
#         })
