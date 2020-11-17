# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectTaskSecurity(http.Controller):
#     @http.route('/de_project_task_security/de_project_task_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_task_security/de_project_task_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_task_security.listing', {
#             'root': '/de_project_task_security/de_project_task_security',
#             'objects': http.request.env['de_project_task_security.de_project_task_security'].search([]),
#         })

#     @http.route('/de_project_task_security/de_project_task_security/objects/<model("de_project_task_security.de_project_task_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_task_security.object', {
#             'object': obj
#         })
