# -*- coding: utf-8 -*-
# from odoo import http


# class DePosCustomerBalance(http.Controller):
#     @http.route('/de_pos_customer_balance/de_pos_customer_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_pos_customer_balance/de_pos_customer_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_pos_customer_balance.listing', {
#             'root': '/de_pos_customer_balance/de_pos_customer_balance',
#             'objects': http.request.env['de_pos_customer_balance.de_pos_customer_balance'].search([]),
#         })

#     @http.route('/de_pos_customer_balance/de_pos_customer_balance/objects/<model("de_pos_customer_balance.de_pos_customer_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_pos_customer_balance.object', {
#             'object': obj
#         })
