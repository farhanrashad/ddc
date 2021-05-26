# -*- coding: utf-8 -*-
# from odoo import http


# class DeInventoryGatepass(http.Controller):
#     @http.route('/de_inventory_gatepass/de_inventory_gatepass/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_inventory_gatepass/de_inventory_gatepass/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_inventory_gatepass.listing', {
#             'root': '/de_inventory_gatepass/de_inventory_gatepass',
#             'objects': http.request.env['de_inventory_gatepass.de_inventory_gatepass'].search([]),
#         })

#     @http.route('/de_inventory_gatepass/de_inventory_gatepass/objects/<model("de_inventory_gatepass.de_inventory_gatepass"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_inventory_gatepass.object', {
#             'object': obj
#         })
