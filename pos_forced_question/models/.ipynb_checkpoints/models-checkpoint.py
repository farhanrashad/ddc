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


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	question_group_ids = fields.Many2many('forced.question.group', string='Question Groups')


class ForcedQuestionGroup(models.Model):
	_name = 'forced.question.group'

	name = fields.Char('Name', required=1)
	questions = fields.Many2many('pos.forced.question',string='Questions')
	active = fields.Boolean('Active',default=1)

	@api.constrains('questions')
	def validate_questions_count(self):
		if len(self.questions) == 0:
			raise ValidationError("Please add atleast one question in question group")


class PosForcedQuestion(models.Model):
	_name = 'pos.forced.question'
	_order = "id desc"

	name = fields.Text('Question', required=1)
	active = fields.Boolean('Active',default=1)
	sequence_number =  fields.Integer('Sequence Number')
	question_groups = fields.Many2many('forced.question.group',string='Available In Question Groups')


	@api.model_create_multi
	def create(self, vals_list):
		for vals in vals_list:
			if vals.get('sequence_number') == False:
				vals['sequence_number'] = self.env[
					'ir.sequence'].next_by_code('pos.forced.question')
		return super(PosForcedQuestion, self).create(vals_list)

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'
	forced_questions = fields.Text('Extra Comments')

	@api.model
	def _order_line_fields(self, line, session_id=None):
		fields_return = super(PosOrderLine,self)._order_line_fields(line,session_id=None)
		fields_return[2].update({'forced_questions':line[2].get('forced_questions','')})
		return fields_return
