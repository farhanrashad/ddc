# -*- coding: utf-8 -*-
from odoo import http

# class DeHelpdeskRepair(http.Controller):
#     @http.route('/de_helpdesk_repair/de_helpdesk_repair/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_helpdesk_repair/de_helpdesk_repair/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_helpdesk_repair.listing', {
#             'root': '/de_helpdesk_repair/de_helpdesk_repair',
#             'objects': http.request.env['de_helpdesk_repair.de_helpdesk_repair'].search([]),
#         })

#     @http.route('/de_helpdesk_repair/de_helpdesk_repair/objects/<model("de_helpdesk_repair.de_helpdesk_repair"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_helpdesk_repair.object', {
#             'object': obj
#         })