# -*- coding: utf-8 -*-
# from odoo import http


# class DeInvoicingCategory(http.Controller):
#     @http.route('/de_invoicing_category/de_invoicing_category/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_invoicing_category/de_invoicing_category/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_invoicing_category.listing', {
#             'root': '/de_invoicing_category/de_invoicing_category',
#             'objects': http.request.env['de_invoicing_category.de_invoicing_category'].search([]),
#         })

#     @http.route('/de_invoicing_category/de_invoicing_category/objects/<model("de_invoicing_category.de_invoicing_category"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_invoicing_category.object', {
#             'object': obj
#         })
