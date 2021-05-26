# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleLot(http.Controller):
#     @http.route('/de_sale_lot/de_sale_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_lot/de_sale_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_lot.listing', {
#             'root': '/de_sale_lot/de_sale_lot',
#             'objects': http.request.env['de_sale_lot.de_sale_lot'].search([]),
#         })

#     @http.route('/de_sale_lot/de_sale_lot/objects/<model("de_sale_lot.de_sale_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_lot.object', {
#             'object': obj
#         })
