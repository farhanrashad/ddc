# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockWarehouseTransfer(http.Controller):
#     @http.route('/de_stock_warehouse_transfer/de_stock_warehouse_transfer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_warehouse_transfer/de_stock_warehouse_transfer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_warehouse_transfer.listing', {
#             'root': '/de_stock_warehouse_transfer/de_stock_warehouse_transfer',
#             'objects': http.request.env['de_stock_warehouse_transfer.de_stock_warehouse_transfer'].search([]),
#         })

#     @http.route('/de_stock_warehouse_transfer/de_stock_warehouse_transfer/objects/<model("de_stock_warehouse_transfer.de_stock_warehouse_transfer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_warehouse_transfer.object', {
#             'object': obj
#         })
