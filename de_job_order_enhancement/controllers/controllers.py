# -*- coding: utf-8 -*-
# from odoo import http


# class DeJobOrderEnhancement(http.Controller):
#     @http.route('/de_job_order_enhancement/de_job_order_enhancement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_job_order_enhancement/de_job_order_enhancement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_job_order_enhancement.listing', {
#             'root': '/de_job_order_enhancement/de_job_order_enhancement',
#             'objects': http.request.env['de_job_order_enhancement.de_job_order_enhancement'].search([]),
#         })

#     @http.route('/de_job_order_enhancement/de_job_order_enhancement/objects/<model("de_job_order_enhancement.de_job_order_enhancement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_job_order_enhancement.object', {
#             'object': obj
#         })
