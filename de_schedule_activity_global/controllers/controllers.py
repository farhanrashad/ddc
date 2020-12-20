# -*- coding: utf-8 -*-
# from odoo import http


# class DeScheduleActivityGlobal(http.Controller):
#     @http.route('/de_schedule_activity_global/de_schedule_activity_global/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_schedule_activity_global/de_schedule_activity_global/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_schedule_activity_global.listing', {
#             'root': '/de_schedule_activity_global/de_schedule_activity_global',
#             'objects': http.request.env['de_schedule_activity_global.de_schedule_activity_global'].search([]),
#         })

#     @http.route('/de_schedule_activity_global/de_schedule_activity_global/objects/<model("de_schedule_activity_global.de_schedule_activity_global"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_schedule_activity_global.object', {
#             'object': obj
#         })
