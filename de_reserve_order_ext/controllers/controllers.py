# -*- coding: utf-8 -*-
# from odoo import http


# class DeReserveOrderExt(http.Controller):
#     @http.route('/de_reserve_order_ext/de_reserve_order_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_reserve_order_ext/de_reserve_order_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_reserve_order_ext.listing', {
#             'root': '/de_reserve_order_ext/de_reserve_order_ext',
#             'objects': http.request.env['de_reserve_order_ext.de_reserve_order_ext'].search([]),
#         })

#     @http.route('/de_reserve_order_ext/de_reserve_order_ext/objects/<model("de_reserve_order_ext.de_reserve_order_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_reserve_order_ext.object', {
#             'object': obj
#         })
