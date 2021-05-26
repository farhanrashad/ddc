# -*- coding: utf-8 -*-
# from odoo import http


# class DePartnerFields(http.Controller):
#     @http.route('/de_partner_fields/de_partner_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_partner_fields/de_partner_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_partner_fields.listing', {
#             'root': '/de_partner_fields/de_partner_fields',
#             'objects': http.request.env['de_partner_fields.de_partner_fields'].search([]),
#         })

#     @http.route('/de_partner_fields/de_partner_fields/objects/<model("de_partner_fields.de_partner_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_partner_fields.object', {
#             'object': obj
#         })
