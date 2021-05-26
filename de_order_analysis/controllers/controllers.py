# -*- coding: utf-8 -*-
# from odoo import http


# class DeOrderAnalysis(http.Controller):
#     @http.route('/de_order_analysis/de_order_analysis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_order_analysis/de_order_analysis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_order_analysis.listing', {
#             'root': '/de_order_analysis/de_order_analysis',
#             'objects': http.request.env['de_order_analysis.de_order_analysis'].search([]),
#         })

#     @http.route('/de_order_analysis/de_order_analysis/objects/<model("de_order_analysis.de_order_analysis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_order_analysis.object', {
#             'object': obj
#         })
