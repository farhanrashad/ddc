# -*- coding: utf-8 -*-
from odoo import http

# class DeReportsEnhancement(http.Controller):
#     @http.route('/de_reports_enhancement/de_reports_enhancement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_reports_enhancement/de_reports_enhancement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_reports_enhancement.listing', {
#             'root': '/de_reports_enhancement/de_reports_enhancement',
#             'objects': http.request.env['de_reports_enhancement.de_reports_enhancement'].search([]),
#         })

#     @http.route('/de_reports_enhancement/de_reports_enhancement/objects/<model("de_reports_enhancement.de_reports_enhancement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_reports_enhancement.object', {
#             'object': obj
#         })