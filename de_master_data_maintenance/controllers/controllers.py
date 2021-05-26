# -*- coding: utf-8 -*-
from odoo import http

# class DeMasterDataMaintenance(http.Controller):
#     @http.route('/de_master_data_maintenance/de_master_data_maintenance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_master_data_maintenance/de_master_data_maintenance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_master_data_maintenance.listing', {
#             'root': '/de_master_data_maintenance/de_master_data_maintenance',
#             'objects': http.request.env['de_master_data_maintenance.de_master_data_maintenance'].search([]),
#         })

#     @http.route('/de_master_data_maintenance/de_master_data_maintenance/objects/<model("de_master_data_maintenance.de_master_data_maintenance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_master_data_maintenance.object', {
#             'object': obj
#         })