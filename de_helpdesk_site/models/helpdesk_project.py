#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskProjectTask(models.Model):
    _inherit = "project.task"

    contact_name = fields.Char(string='Contact Name', readonly=False)
    contact_no = fields.Char(string='Contact no', readonly=False)
    