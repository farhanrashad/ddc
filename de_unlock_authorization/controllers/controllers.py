# -*- coding: utf-8 -*-
from odoo import http

# class DeAccountInvoiceFilter(http.Controller):
#     @http.route('/de_account_invoice_filter/de_account_invoice_filter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_invoice_filter/de_account_invoice_filter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_invoice_filter.listing', {
#             'root': '/de_account_invoice_filter/de_account_invoice_filter',
#             'objects': http.request.env['de_account_invoice_filter.de_account_invoice_filter'].search([]),
#         })

#     @http.route('/de_account_invoice_filter/de_account_invoice_filter/objects/<model("de_account_invoice_filter.de_account_invoice_filter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_invoice_filter.object', {
#             'object': obj
#         })