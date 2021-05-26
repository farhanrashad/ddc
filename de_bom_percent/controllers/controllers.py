# -*- coding: utf-8 -*-
# from odoo import http


# class DeBomPercent(http.Controller):
#     @http.route('/de_bom_percent/de_bom_percent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_bom_percent/de_bom_percent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_bom_percent.listing', {
#             'root': '/de_bom_percent/de_bom_percent',
#             'objects': http.request.env['de_bom_percent.de_bom_percent'].search([]),
#         })

#     @http.route('/de_bom_percent/de_bom_percent/objects/<model("de_bom_percent.de_bom_percent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_bom_percent.object', {
#             'object': obj
#         })
