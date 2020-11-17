# -*- coding: utf-8 -*-
# from odoo import http


# class DeHelpdeskRmWarranty(http.Controller):
#     @http.route('/de_helpdesk_rm_warranty/de_helpdesk_rm_warranty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_helpdesk_rm_warranty/de_helpdesk_rm_warranty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_helpdesk_rm_warranty.listing', {
#             'root': '/de_helpdesk_rm_warranty/de_helpdesk_rm_warranty',
#             'objects': http.request.env['de_helpdesk_rm_warranty.de_helpdesk_rm_warranty'].search([]),
#         })

#     @http.route('/de_helpdesk_rm_warranty/de_helpdesk_rm_warranty/objects/<model("de_helpdesk_rm_warranty.de_helpdesk_rm_warranty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_helpdesk_rm_warranty.object', {
#             'object': obj
#         })
