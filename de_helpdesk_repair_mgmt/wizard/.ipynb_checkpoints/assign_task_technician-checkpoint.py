# -*- coding: utf-8 -*-
# Part of Dynexcel. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class AssignTechnician(models.TransientModel):
    _name = 'assign.task.technician'
    _description = "Assign Task Technician"
    
    user_id = fields.Many2one('res.users',string='Technician', required=True)
    
    def assign_technician(self):
        tasks = self.env['project.task'].browse(self.env.context.get('active_ids'))
        tasks.update({
            'user_id': self.user_id.id
        })
