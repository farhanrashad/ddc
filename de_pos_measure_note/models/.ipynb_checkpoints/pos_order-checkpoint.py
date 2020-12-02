# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from itertools import groupby
from re import search

from odoo import api, fields, models


class PosOrderNote(models.Model):
    """In this class a new model is created in pos to create multiple
    order notes in the backend"""

    _name = 'pos.order.note'
    _rec_name = 'pos_note'

    pos_note = fields.Char(string='Multiple Order Note In POS',
                           help='Add the description of the order note')