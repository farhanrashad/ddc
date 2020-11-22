# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError
	
class PosForcedQuestion(models.Model):
	_inherit = 'pos.forced.question'

	wk_extra_price = fields.Float('Extra Price', default=0)
	currency_id = fields.Many2one(
	'res.currency', 'Currency',
	default=lambda self: self.env.user.company_id.currency_id.id)

	@api.constrains('wk_extra_price')
	def validate_extra_price(self):
		if self.wk_extra_price<0:
			raise ValidationError("Extra Price can not be less than zero.")
