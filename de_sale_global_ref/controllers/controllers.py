# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleGlobalRef(http.Controller):
#     @http.route('/de_sale_global_ref/de_sale_global_ref/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_global_ref/de_sale_global_ref/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_global_ref.listing', {
#             'root': '/de_sale_global_ref/de_sale_global_ref',
#             'objects': http.request.env['de_sale_global_ref.de_sale_global_ref'].search([]),
#         })

#     @http.route('/de_sale_global_ref/de_sale_global_ref/objects/<model("de_sale_global_ref.de_sale_global_ref"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_global_ref.object', {
#             'object': obj
#         })
