# -*- coding: utf-8 -*-
from odoo import http

# class DeProductDimensions(http.Controller):
#     @http.route('/de_product_dimensions/de_product_dimensions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_dimensions/de_product_dimensions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_dimensions.listing', {
#             'root': '/de_product_dimensions/de_product_dimensions',
#             'objects': http.request.env['de_product_dimensions.de_product_dimensions'].search([]),
#         })

#     @http.route('/de_product_dimensions/de_product_dimensions/objects/<model("de_product_dimensions.de_product_dimensions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_dimensions.object', {
#             'object': obj
#         })