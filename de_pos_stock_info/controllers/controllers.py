# -*- coding: utf-8 -*-
# from odoo import http


# class DePosStockInfo(http.Controller):
#     @http.route('/de_pos_stock_info/de_pos_stock_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_pos_stock_info/de_pos_stock_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_pos_stock_info.listing', {
#             'root': '/de_pos_stock_info/de_pos_stock_info',
#             'objects': http.request.env['de_pos_stock_info.de_pos_stock_info'].search([]),
#         })

#     @http.route('/de_pos_stock_info/de_pos_stock_info/objects/<model("de_pos_stock_info.de_pos_stock_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_pos_stock_info.object', {
#             'object': obj
#         })
