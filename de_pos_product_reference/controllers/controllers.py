# -*- coding: utf-8 -*-
# from odoo import http


# class DePosProductReference(http.Controller):
#     @http.route('/de_pos_product_reference/de_pos_product_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_pos_product_reference/de_pos_product_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_pos_product_reference.listing', {
#             'root': '/de_pos_product_reference/de_pos_product_reference',
#             'objects': http.request.env['de_pos_product_reference.de_pos_product_reference'].search([]),
#         })

#     @http.route('/de_pos_product_reference/de_pos_product_reference/objects/<model("de_pos_product_reference.de_pos_product_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_pos_product_reference.object', {
#             'object': obj
#         })
