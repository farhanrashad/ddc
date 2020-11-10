# -*- coding: utf-8 -*-
# from odoo import http


# class DeHelpdeskRepairManagement(http.Controller):
#     @http.route('/de_helpdesk_repair_management/de_helpdesk_repair_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_helpdesk_repair_management/de_helpdesk_repair_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_helpdesk_repair_management.listing', {
#             'root': '/de_helpdesk_repair_management/de_helpdesk_repair_management',
#             'objects': http.request.env['de_helpdesk_repair_management.de_helpdesk_repair_management'].search([]),
#         })

#     @http.route('/de_helpdesk_repair_management/de_helpdesk_repair_management/objects/<model("de_helpdesk_repair_management.de_helpdesk_repair_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_helpdesk_repair_management.object', {
#             'object': obj
#         })
