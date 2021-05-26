# -*- coding: utf-8 -*-
from odoo import http

# class DeLotAttribute(http.Controller):
#     @http.route('/de_lot_attribute/de_lot_attribute/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_lot_attribute/de_lot_attribute/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_lot_attribute.listing', {
#             'root': '/de_lot_attribute/de_lot_attribute',
#             'objects': http.request.env['de_lot_attribute.de_lot_attribute'].search([]),
#         })

#     @http.route('/de_lot_attribute/de_lot_attribute/objects/<model("de_lot_attribute.de_lot_attribute"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_lot_attribute.object', {
#             'object': obj
#         })