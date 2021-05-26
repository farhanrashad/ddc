# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleTags(http.Controller):
#     @http.route('/de_sale_tags/de_sale_tags/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_tags/de_sale_tags/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_tags.listing', {
#             'root': '/de_sale_tags/de_sale_tags',
#             'objects': http.request.env['de_sale_tags.de_sale_tags'].search([]),
#         })

#     @http.route('/de_sale_tags/de_sale_tags/objects/<model("de_sale_tags.de_sale_tags"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_tags.object', {
#             'object': obj
#         })
