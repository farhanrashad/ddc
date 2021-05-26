# -*- coding: utf-8 -*-
# from odoo import http


# class DeMrpCost(http.Controller):
#     @http.route('/de_mrp_cost/de_mrp_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mrp_cost/de_mrp_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mrp_cost.listing', {
#             'root': '/de_mrp_cost/de_mrp_cost',
#             'objects': http.request.env['de_mrp_cost.de_mrp_cost'].search([]),
#         })

#     @http.route('/de_mrp_cost/de_mrp_cost/objects/<model("de_mrp_cost.de_mrp_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mrp_cost.object', {
#             'object': obj
#         })
