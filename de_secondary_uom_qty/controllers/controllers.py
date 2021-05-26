# -*- coding: utf-8 -*-
# from odoo import http


# class DeSecondaryUom(http.Controller):
#     @http.route('/de_secondary_uom/de_secondary_uom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_secondary_uom/de_secondary_uom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_secondary_uom.listing', {
#             'root': '/de_secondary_uom/de_secondary_uom',
#             'objects': http.request.env['de_secondary_uom.de_secondary_uom'].search([]),
#         })

#     @http.route('/de_secondary_uom/de_secondary_uom/objects/<model("de_secondary_uom.de_secondary_uom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_secondary_uom.object', {
#             'object': obj
#         })
