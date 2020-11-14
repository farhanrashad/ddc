# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, fields, api, _

class PosOrder(models.Model):
    _inherit = "pos.order"

    def create_picking(self):
        super(PosOrder, self).create_picking()
        for record in self:
            record.picking_id.date_done = record.date_order
