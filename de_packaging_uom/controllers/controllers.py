# -*- coding: utf-8 -*-
from odoo import http

# class DePackagingUom(http.Controller):
#     @http.route('/de_packaging_uom/de_packaging_uom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_packaging_uom/de_packaging_uom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_packaging_uom.listing', {
#             'root': '/de_packaging_uom/de_packaging_uom',
#             'objects': http.request.env['de_packaging_uom.de_packaging_uom'].search([]),
#         })

#     @http.route('/de_packaging_uom/de_packaging_uom/objects/<model("de_packaging_uom.de_packaging_uom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_packaging_uom.object', {
#             'object': obj
#         })