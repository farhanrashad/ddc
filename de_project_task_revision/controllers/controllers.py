# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectTaskRevision(http.Controller):
#     @http.route('/de_project_task_revision/de_project_task_revision/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_task_revision/de_project_task_revision/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_task_revision.listing', {
#             'root': '/de_project_task_revision/de_project_task_revision',
#             'objects': http.request.env['de_project_task_revision.de_project_task_revision'].search([]),
#         })

#     @http.route('/de_project_task_revision/de_project_task_revision/objects/<model("de_project_task_revision.de_project_task_revision"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_task_revision.object', {
#             'object': obj
#         })
