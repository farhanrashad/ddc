# -*- coding: utf-8 -*-
from odoo import http

# class DeProductWeight(http.Controller):
#     @http.route('/de_product_weight/de_product_weight/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_weight/de_product_weight/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_weight.listing', {
#             'root': '/de_product_weight/de_product_weight',
#             'objects': http.request.env['de_product_weight.de_product_weight'].search([]),
#         })

#     @http.route('/de_product_weight/de_product_weight/objects/<model("de_product_weight.de_product_weight"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_weight.object', {
#             'object': obj
#         })