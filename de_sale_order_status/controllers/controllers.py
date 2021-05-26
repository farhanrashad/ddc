# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleOrderStatus(http.Controller):
#     @http.route('/de_sale_order_status/de_sale_order_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_order_status/de_sale_order_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_order_status.listing', {
#             'root': '/de_sale_order_status/de_sale_order_status',
#             'objects': http.request.env['de_sale_order_status.de_sale_order_status'].search([]),
#         })

#     @http.route('/de_sale_order_status/de_sale_order_status/objects/<model("de_sale_order_status.de_sale_order_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_order_status.object', {
#             'object': obj
#         })
