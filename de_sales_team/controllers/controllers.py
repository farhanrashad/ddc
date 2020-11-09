# -*- coding: utf-8 -*-
from odoo import http

# class DeSalesTeam(http.Controller):
#     @http.route('/de_sales_team/de_sales_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sales_team/de_sales_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sales_team.listing', {
#             'root': '/de_sales_team/de_sales_team',
#             'objects': http.request.env['de_sales_team.de_sales_team'].search([]),
#         })

#     @http.route('/de_sales_team/de_sales_team/objects/<model("de_sales_team.de_sales_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sales_team.object', {
#             'object': obj
#         })