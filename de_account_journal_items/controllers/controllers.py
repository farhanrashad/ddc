# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountJournalItems(http.Controller):
#     @http.route('/de_account_journal_items/de_account_journal_items/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_journal_items/de_account_journal_items/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_journal_items.listing', {
#             'root': '/de_account_journal_items/de_account_journal_items',
#             'objects': http.request.env['de_account_journal_items.de_account_journal_items'].search([]),
#         })

#     @http.route('/de_account_journal_items/de_account_journal_items/objects/<model("de_account_journal_items.de_account_journal_items"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_journal_items.object', {
#             'object': obj
#         })
