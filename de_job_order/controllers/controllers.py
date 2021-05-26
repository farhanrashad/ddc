# -*- coding: utf-8 -*-
from odoo import http

# class DeMrpBomCalculation(http.Controller):
#     @http.route('/de_mrp_bom_calculation/de_mrp_bom_calculation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mrp_bom_calculation/de_mrp_bom_calculation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mrp_bom_calculation.listing', {
#             'root': '/de_mrp_bom_calculation/de_mrp_bom_calculation',
#             'objects': http.request.env['de_mrp_bom_calculation.de_mrp_bom_calculation'].search([]),
#         })

#     @http.route('/de_mrp_bom_calculation/de_mrp_bom_calculation/objects/<model("de_mrp_bom_calculation.de_mrp_bom_calculation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mrp_bom_calculation.object', {
#             'object': obj
#         })