# -*- coding: utf-8 -*-

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
from functools import partial
import psycopg2
import pytz
import odoo.addons.decimal_precision as dp



class POSConfigInherit(models.Model):
	_inherit = 'pos.config'
	
	enable_reservation = fields.Boolean('Allow Reserve Order')
	reservation_location = fields.Many2one('stock.location','Location to store reserve products',domain=[('usage', '!=', 'view')])
	cancel_charge_type = fields.Selection([('percentage', "Percentage"), ('fixed', "Fixed")], string='Cancellation Charge Type', default='fixed')
	cancel_charges = fields.Float('Cancellation Charges')
	cancel_charges_product = fields.Many2one('product.product','Cancellation Charges Product',domain=[('type', '=', 'service'),('available_in_pos','=',True)])
	reserve_charge_type = fields.Selection([('percentage', "Percentage"), ('fixed', "Fixed")], string='Reservation Charge Type', default='fixed')
	min_reserve_charges = fields.Float('Minimum amount to reserve order')
	last_days = fields.Integer('Load Reserve Orders for Last')


	def open_session_cb(self):
		""" new session button

		create one if none exist
		access cash control interface if enabled or start a session
		"""
		self.ensure_one()
		payment = self.env['pos.payment'].search([])
		session = self.env['pos.session'].search([])

		if not self.current_session_id:
			if not self.company_has_template:
				raise UserError(_("A Chart of Accounts is not yet installed in your current company. Please install a "
								  "Chart of Accounts through the Invoicing/Accounting settings before launching a PoS session." ))
			self._check_company_journal()
			self._check_company_invoice_journal()
			self._check_company_payment()
			self._check_currencies()
			self.env['pos.session'].create({
				'user_id': self.env.uid,
				'config_id': self.id
			})
			if self.current_session_id.state == 'opened':
				return self.open_ui()
		return self._open_session(self.current_session_id.id)