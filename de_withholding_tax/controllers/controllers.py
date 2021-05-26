# -*- coding: utf-8 -*-
# from odoo import http


# class DeWithholdingTax(http.Controller):
#     @http.route('/de_withholding_tax/de_withholding_tax/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_withholding_tax/de_withholding_tax/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_withholding_tax.listing', {
#             'root': '/de_withholding_tax/de_withholding_tax',
#             'objects': http.request.env['de_withholding_tax.de_withholding_tax'].search([]),
#         })

#     @http.route('/de_withholding_tax/de_withholding_tax/objects/<model("de_withholding_tax.de_withholding_tax"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_withholding_tax.object', {
#             'object': obj
#         })
