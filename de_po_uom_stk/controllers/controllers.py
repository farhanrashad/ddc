# -*- coding: utf-8 -*-
# from odoo import http


# class DePoUomStk(http.Controller):
#     @http.route('/de_po_uom_stk/de_po_uom_stk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_po_uom_stk/de_po_uom_stk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_po_uom_stk.listing', {
#             'root': '/de_po_uom_stk/de_po_uom_stk',
#             'objects': http.request.env['de_po_uom_stk.de_po_uom_stk'].search([]),
#         })

#     @http.route('/de_po_uom_stk/de_po_uom_stk/objects/<model("de_po_uom_stk.de_po_uom_stk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_po_uom_stk.object', {
#             'object': obj
#         })
