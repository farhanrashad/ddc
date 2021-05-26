# -*- coding: utf-8 -*-
# from odoo import http


# class DeDeliveryProductName(http.Controller):
#     @http.route('/de_delivery_product_name/de_delivery_product_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_delivery_product_name/de_delivery_product_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_delivery_product_name.listing', {
#             'root': '/de_delivery_product_name/de_delivery_product_name',
#             'objects': http.request.env['de_delivery_product_name.de_delivery_product_name'].search([]),
#         })

#     @http.route('/de_delivery_product_name/de_delivery_product_name/objects/<model("de_delivery_product_name.de_delivery_product_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_delivery_product_name.object', {
#             'object': obj
#         })
