# -*- coding: utf-8 -*-
from odoo import http

# class DeLinkProduct(http.Controller):
#     @http.route('/de_link_product/de_link_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_link_product/de_link_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_link_product.listing', {
#             'root': '/de_link_product/de_link_product',
#             'objects': http.request.env['de_link_product.de_link_product'].search([]),
#         })

#     @http.route('/de_link_product/de_link_product/objects/<model("de_link_product.de_link_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_link_product.object', {
#             'object': obj
#         })