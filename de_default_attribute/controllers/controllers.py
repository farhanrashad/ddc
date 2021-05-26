# -*- coding: utf-8 -*-
from odoo import http

# class DeDefaultAttribute(http.Controller):
#     @http.route('/de_default_attribute/de_default_attribute/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_default_attribute/de_default_attribute/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_default_attribute.listing', {
#             'root': '/de_default_attribute/de_default_attribute',
#             'objects': http.request.env['de_default_attribute.de_default_attribute'].search([]),
#         })

#     @http.route('/de_default_attribute/de_default_attribute/objects/<model("de_default_attribute.de_default_attribute"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_default_attribute.object', {
#             'object': obj
#         })