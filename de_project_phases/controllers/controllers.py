# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectPhases(http.Controller):
#     @http.route('/de_project_phases/de_project_phases/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_phases/de_project_phases/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_phases.listing', {
#             'root': '/de_project_phases/de_project_phases',
#             'objects': http.request.env['de_project_phases.de_project_phases'].search([]),
#         })

#     @http.route('/de_project_phases/de_project_phases/objects/<model("de_project_phases.de_project_phases"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_phases.object', {
#             'object': obj
#         })
