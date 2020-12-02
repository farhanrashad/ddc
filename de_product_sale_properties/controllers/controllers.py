# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductSaleConfiguration(http.Controller):
#     @http.route('/de_product_sale_configuration/de_product_sale_configuration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_sale_configuration/de_product_sale_configuration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_sale_configuration.listing', {
#             'root': '/de_product_sale_configuration/de_product_sale_configuration',
#             'objects': http.request.env['de_product_sale_configuration.de_product_sale_configuration'].search([]),
#         })

#     @http.route('/de_product_sale_configuration/de_product_sale_configuration/objects/<model("de_product_sale_configuration.de_product_sale_configuration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_sale_configuration.object', {
#             'object': obj
#         })
