#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskProjectTask(models.Model):
    _inherit = "project.task"

    contact_name = fields.Char('Contact Name')
    contact_no = fields.Char('Contact no')
    