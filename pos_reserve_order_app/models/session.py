# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
from collections import defaultdict

class PosSessionInherit(models.Model):
	_inherit = 'pos.session'

	payment_ids = fields.Many2one('pos.payment')

	# @api.model
	# def create(self, vals):
	# 	res = super(PosSessionInherit, self).create(vals)
	# 	orders = self.env['pos.order'].search([
	# 		('state', '=', 'reserved'), ('user_id', '=', request.env.uid)])
	# 	orders.write({'session_id': res.id})
	# 	return res

	@api.depends('order_ids.payment_ids.amount')
	def _compute_total_payments_amount(self):
		pos_order = self.env['pos.payment'].search([])
		for session in self:
			payment_ids = self.env['pos.payment'].search([('session_id','=', session.id)])
			session.total_payments_amount = sum([line.amount for line in payment_ids])

	# def action_view_order(self):
	# 	pos_order = self.env['pos.order'].search([])
	# 	for order in pos_order:
	# 		if order.secondary_session == self:
	# 			return{
	# 				'name': _('Orders'),
	# 				'res_model': 'pos.order',
	# 				'view_mode': 'tree,form',
	# 				'views': [
	# 					(self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
	# 					(self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
	# 					],
	# 				'type': 'ir.actions.act_window',
	# 				'domain': [('secondary_session', 'in', self.ids)],
	# 			}
	# 		else:
	# 			return{
	# 				'name': _('Orders'),
	# 				'res_model': 'pos.order',
	# 				'view_mode': 'tree,form',
	# 				'views': [
	# 					(self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
	# 					(self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
	# 					],
	# 				'type': 'ir.actions.act_window',
	# 				'domain': [('session_id', 'in', self.ids)],
	# 			}
				
	def _compute_order_count(self):
		orders_data = self.env['pos.order'].read_group([('session_id', 'in', self.ids)], ['session_id'], ['session_id'])
		sessions_data = {order_data['session_id'][0]: order_data['session_id_count'] for order_data in orders_data}

		secondary_data = self.env['pos.order'].read_group([('secondary_session', 'in', self.ids)], ['secondary_session'], ['secondary_session'])
		secondary_sessions_data = {order_data['secondary_session'][0]: order_data['secondary_session_count'] for order_data in secondary_data}
		for session in self:
			if secondary_data:
				session.order_count = secondary_sessions_data.get(session.id)
			else:
				session.order_count = sessions_data.get(session.id, 0)

	def _accumulate_amounts(self, data):
		# Accumulate the amounts for each accounting lines group
		# Each dict maps `key` -> `amounts`, where `key` is the group key.
		# E.g. `combine_receivables` is derived from pos.payment records
		# in the self.order_ids with group key of the `payment_method_id`
		# field of the pos.payment record.
		amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0}
		tax_amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0, 'base_amount': 0.0, 'base_amount_converted': 0.0}
		split_receivables = defaultdict(amounts)
		split_receivables_cash = defaultdict(amounts)
		combine_receivables = defaultdict(amounts)
		combine_receivables_cash = defaultdict(amounts)
		invoice_receivables = defaultdict(amounts)
		sales = defaultdict(amounts)
		taxes = defaultdict(tax_amounts)
		stock_expense = defaultdict(amounts)
		stock_output = defaultdict(amounts)
		# Track the receivable lines of the invoiced orders' account moves for reconciliation
		# These receivable lines are reconciled to the corresponding invoice receivable lines
		# of this session's move_id.
		order_account_move_receivable_lines = defaultdict(lambda: self.env['account.move.line'])
		rounded_globally = self.company_id.tax_calculation_rounding_method == 'round_globally'
		for order in self.order_ids.filtered(lambda stat: stat.state != 'reserved'):
			# if order.state != 'reserved':
				# Combine pos receivable lines
				# Separate cash payments for cash reconciliation later.
			for payment in order.payment_ids:
				amount, date = payment.amount, payment.payment_date
				if payment.payment_method_id.split_transactions:
					if payment.payment_method_id.is_cash_count:
						split_receivables_cash[payment] = self._update_amounts(split_receivables_cash[payment], {'amount': amount}, date)
					else:
						split_receivables[payment] = self._update_amounts(split_receivables[payment], {'amount': amount}, date)
				else:
					key = payment.payment_method_id
					if payment.payment_method_id.is_cash_count:
						combine_receivables_cash[key] = self._update_amounts(combine_receivables_cash[key], {'amount': amount}, date)
					else:
						combine_receivables[key] = self._update_amounts(combine_receivables[key], {'amount': amount}, date)

			if order.is_invoiced:
				# Combine invoice receivable lines
				key = order.partner_id.property_account_receivable_id.id
				invoice_receivables[key] = self._update_amounts(invoice_receivables[key], {'amount': order._get_amount_receivable()}, order.date_order)
				# side loop to gather receivable lines by account for reconciliation
				for move_line in order.account_move.line_ids.filtered(lambda aml: aml.account_id.internal_type == 'receivable' and not aml.reconciled):
					order_account_move_receivable_lines[move_line.account_id.id] |= move_line
			else:
				order_taxes = defaultdict(tax_amounts)
				for order_line in order.lines:
					line = self._prepare_line(order_line)
					# Combine sales/refund lines
					sale_key = (
						# account
						line['income_account_id'],
						# sign
						-1 if line['amount'] < 0 else 1,
						# for taxes
						tuple((tax['id'], tax['account_id'], tax['tax_repartition_line_id']) for tax in line['taxes']),
					)
					sales[sale_key] = self._update_amounts(sales[sale_key], {'amount': line['amount']}, line['date_order'])
					# Combine tax lines
					for tax in line['taxes']:
						tax_key = (tax['account_id'], tax['tax_repartition_line_id'], tax['id'], tuple(tax['tag_ids']))
						order_taxes[tax_key] = self._update_amounts(
							order_taxes[tax_key],
							{'amount': tax['amount'], 'base_amount': tax['base']},
							tax['date_order'],
							round=not rounded_globally
						)
				for tax_key, amounts in order_taxes.items():
					if rounded_globally:
						amounts = self._round_amounts(amounts)
					for amount_key, amount in amounts.items():
						taxes[tax_key][amount_key] += amount

				if self.company_id.anglo_saxon_accounting and order.picking_id.id:
					# Combine stock lines
					stock_moves = self.env['stock.move'].search([
						('picking_id', '=', order.picking_id.id),
						('company_id.anglo_saxon_accounting', '=', True),
						('product_id.categ_id.property_valuation', '=', 'real_time')
					])
					for move in stock_moves:
						exp_key = move.product_id.property_account_expense_id or move.product_id.categ_id.property_account_expense_categ_id
						out_key = move.product_id.categ_id.property_stock_account_output_categ_id
						amount = -sum(move.stock_valuation_layer_ids.mapped('value'))
						stock_expense[exp_key] = self._update_amounts(stock_expense[exp_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
						stock_output[out_key] = self._update_amounts(stock_output[out_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)

				# Increasing current partner's customer_rank
				order.partner_id._increase_rank('customer_rank')

		MoveLine = self.env['account.move.line'].with_context(check_move_validity=False)

		data.update({
			'taxes':                               taxes,
			'sales':                               sales,
			'stock_expense':                       stock_expense,
			'split_receivables':                   split_receivables,
			'combine_receivables':                 combine_receivables,
			'split_receivables_cash':              split_receivables_cash,
			'combine_receivables_cash':            combine_receivables_cash,
			'invoice_receivables':                 invoice_receivables,
			'stock_output':                        stock_output,
			'order_account_move_receivable_lines': order_account_move_receivable_lines,
			'MoveLine':                            MoveLine
		})
		return data
			

	def _confirm_orders(self):
		for session in self:
			company_id = session.config_id.journal_id.company_id.id
			orders = session.order_ids.filtered(lambda order: order.state == 'paid')
			journal_id = self.env['ir.config_parameter'].sudo().get_param(
				'pos.closing.journal_id_%s' % company_id, default=session.config_id.journal_id.id)
			if not journal_id:
				raise UserError(_("You have to set a Sale Journal for the POS:%s") % (session.config_id.name,))

			move = self.env['pos.order'].with_context(force_company=company_id)._create_account_move(session.start_at, session.name, int(journal_id), company_id)
			orders.with_context(force_company=company_id)._create_account_move_line(session, move)
			
			for order in session.order_ids.filtered(lambda o: o.state not in ['done', 'invoiced']):
				if order.state  in ('paid'):
					order.action_pos_order_done()
			
			orders_to_reconcile = session.order_ids._filtered_for_reconciliation()
			orders_to_reconcile.sudo()._reconcile_payments()
