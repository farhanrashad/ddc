# -*- coding: utf-8 -*-
# from odoo import http


# class DeHelpdeskRepairCustomViews(http.Controller):
#     @http.route('/de_helpdesk_repair_custom_views/de_helpdesk_repair_custom_views/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_helpdesk_repair_custom_views/de_helpdesk_repair_custom_views/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_helpdesk_repair_custom_views.listing', {
#             'root': '/de_helpdesk_repair_custom_views/de_helpdesk_repair_custom_views',
#             'objects': http.request.env['de_helpdesk_repair_custom_views.de_helpdesk_repair_custom_views'].search([]),
#         })

#     @http.route('/de_helpdesk_repair_custom_views/de_helpdesk_repair_custom_views/objects/<model("de_helpdesk_repair_custom_views.de_helpdesk_repair_custom_views"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_helpdesk_repair_custom_views.object', {
#             'object': obj
#         })
