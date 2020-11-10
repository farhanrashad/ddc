# -*- coding: utf-8 -*-
# from odoo import http


# class DePosSaleForcedQuestion(http.Controller):
#     @http.route('/de_pos_sale_forced_question/de_pos_sale_forced_question/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_pos_sale_forced_question/de_pos_sale_forced_question/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_pos_sale_forced_question.listing', {
#             'root': '/de_pos_sale_forced_question/de_pos_sale_forced_question',
#             'objects': http.request.env['de_pos_sale_forced_question.de_pos_sale_forced_question'].search([]),
#         })

#     @http.route('/de_pos_sale_forced_question/de_pos_sale_forced_question/objects/<model("de_pos_sale_forced_question.de_pos_sale_forced_question"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_pos_sale_forced_question.object', {
#             'object': obj
#         })
