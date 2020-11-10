# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.exceptions import UserError
from odoo.tools import float_is_zero



class pos_config(models.Model):
	_inherit = 'pos.config'

	wallet_credit_in_return = fields.Boolean("Credit Return Order Amount in Customer's Wallet ?")


class PosMakePayment(models.TransientModel):
	_inherit = 'pos.make.payment'

	credit_to_wallet = fields.Boolean("Credit to Wallet")

	def check(self):
		"""Check the order:
		if the order is not paid: continue payment,
		if the order is paid print ticket.
		"""
		self.ensure_one()

		if self.payment_method_id.wallet and self.credit_to_wallet : 
			raise UserError(_("You Can not credit to wallet using : "+self.payment_method_id.name + " (Wallet Journal)"))
			
		order = self.env['pos.order'].browse(self.env.context.get('active_id', False))
		currency = order.currency_id

		init_data = self.read()[0]
		if not float_is_zero(init_data['amount'], precision_rounding=currency.rounding):
			order.add_payment({
				'pos_order_id': order.id,
				'amount': order._get_rounded_amount(self.amount),
				'name': self.payment_name,
				'payment_method_id': self.payment_method_id.id,
			})

		wallet_transaction_obj = self.env['pos.wallet.transaction']
		vals = {
			'wallet_type': 'credit',
			'partner_id': order.partner_id.id,
			'pos_order_id' : order.id,
			'reference' : 'pos_order',
			'amount' :  -self.amount,
			'currency_id' : order.currency_id.id,
			'status': 'done'
		}
		wallet_create = wallet_transaction_obj.sudo().create(vals)
		total_amount = order.partner_id.wallet_balance + float(-self.amount) # Total Amount
		order.partner_id.write({'wallet_balance': total_amount })	
			
		if order._is_pos_order_paid():
			order.action_pos_order_paid()
			return {'type': 'ir.actions.act_window_close'}

		return self.launch_payment()


class pos_order(models.Model):
	_inherit = 'pos.order'
	
	wallet_used = fields.Float('Wallet Amount Used')
	wallet_transaction_id = fields.Many2one('pos.wallet.transaction', 'Wallet Transaction')
	return_credit = fields.Boolean("Return Credit")

	@api.model
	def _order_fields(self, ui_order):
		res = super(pos_order, self)._order_fields(ui_order)		
		if ui_order.get('return_credit'):
			res['return_credit'] = int(ui_order['return_credit'])
		return res

	@api.model
	def create_from_ui(self, orders, draft=False):
		wallet_transaction_obj = self.env['pos.wallet.transaction']
		order_ids = super(pos_order, self).create_from_ui(orders,draft)
		flag = False
		for order_id in order_ids:
			pos_order_id = self.browse(order_id.get('id'))
			amount =0.0
			for pos_wallet in pos_order_id.payment_ids:
				if pos_wallet.payment_method_id.wallet == True:
					amount += pos_wallet.amount
					flag = True
			if flag:
				vals = {
					'wallet_type': 'debit',
					'partner_id': pos_order_id.partner_id.id,
					'pos_order_id' : order_id.get('id'),
					'reference' : 'pos_order',
					'amount' : amount,
					'currency_id' : pos_order_id.pricelist_id.currency_id.id,
					'status': 'done'
				}
				wallet_create = wallet_transaction_obj.sudo().create(vals)
				pos_order_id.write({'wallet_used':amount, 'wallet_transaction_id':wallet_create.id })       
				
			if pos_order_id.amount_total < 0 and pos_order_id.return_credit :
				vals = {
					'wallet_type': 'credit',
					'partner_id': pos_order_id.partner_id.id,
					'pos_order_id' : pos_order_id.id,
					'reference' : 'pos_order',
					'amount' :  -pos_order_id.amount_total,
					'currency_id' : pos_order_id.currency_id.id,
					'status': 'done'
				}
				wallet_create = wallet_transaction_obj.sudo().create(vals)
				total_amount = pos_order_id.partner_id.wallet_balance + float(-pos_order_id.amount_total) # Total Amount
				pos_order_id.partner_id.write({'wallet_balance': total_amount })	


		return order_ids
			
	
class res_partner(models.Model):
	_inherit = 'res.partner'

	wallet_balance = fields.Float('Wallet Balance')
	wallet_transaction_count = fields.Integer(compute='_compute_wallet_transaction_count', string="Wallet")

	def _compute_wallet_transaction_count(self):
		wallet_data = self.env['pos.wallet.transaction'].search([('partner_id', 'in', self.ids)])
		for partner in self:
			partner.wallet_transaction_count = len(wallet_data)
			

class account_journal(models.Model):
	_inherit = 'account.journal'

	wallet = fields.Boolean(string='Wallet Journal')


class pos_payment_method(models.Model):
	_inherit = 'pos.payment.method'

	wallet = fields.Boolean(string='Wallet Journal',related = "cash_journal_id.wallet")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
