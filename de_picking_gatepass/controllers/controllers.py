# -*- coding: utf-8 -*-
# from odoo import http


# class DePickingGatepass(http.Controller):
#     @http.route('/de_picking_gatepass/de_picking_gatepass/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_picking_gatepass/de_picking_gatepass/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_picking_gatepass.listing', {
#             'root': '/de_picking_gatepass/de_picking_gatepass',
#             'objects': http.request.env['de_picking_gatepass.de_picking_gatepass'].search([]),
#         })

#     @http.route('/de_picking_gatepass/de_picking_gatepass/objects/<model("de_picking_gatepass.de_picking_gatepass"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_picking_gatepass.object', {
#             'object': obj
#         })
