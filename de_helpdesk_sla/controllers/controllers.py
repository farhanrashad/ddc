# -*- coding: utf-8 -*-
# from odoo import http


# class DeHelpdeskSla(http.Controller):
#     @http.route('/de_helpdesk_sla/de_helpdesk_sla/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_helpdesk_sla/de_helpdesk_sla/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_helpdesk_sla.listing', {
#             'root': '/de_helpdesk_sla/de_helpdesk_sla',
#             'objects': http.request.env['de_helpdesk_sla.de_helpdesk_sla'].search([]),
#         })

#     @http.route('/de_helpdesk_sla/de_helpdesk_sla/objects/<model("de_helpdesk_sla.de_helpdesk_sla"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_helpdesk_sla.object', {
#             'object': obj
#         })
