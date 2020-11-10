# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime

class AccountPayment(models.Model):
	_inherit ='account.payment'

	description = fields.Text(string='Description')

			
class pos_wallet_transaction(models.Model):
	_name='pos.wallet.transaction'
	_description ='POS Wallet Transaction' 

	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('pos.wallet.transaction') or 'New'
		res = super(pos_wallet_transaction, self).create(vals)
		return res

	def wallet_recharge(self, partner_id, wallet, journal,descr):

		wallet_transaction_obj = self.env['pos.wallet.transaction']
		
		partner = self.env['res.partner'].browse(partner_id['id'])
		vals = {
			'wallet_type': 'credit',
			'partner_id': partner.id,
			#'pos_order_id' : order_id,
			'reference' : 'manual',
			'amount' : wallet,
			'currency_id' : partner.property_product_pricelist.currency_id.id,
			'status': 'done'
		}
		wallet_create = wallet_transaction_obj.sudo().create(vals)

		account_payment_obj = self.env['account.payment']
		date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')

		if journal == 'cash':
			cash_journal_ids = self.env['account.journal'].search([('type','=','cash')])
			if cash_journal_ids:
				journal = cash_journal_ids[0].id

		if journal == 'check':
			bank_journal_ids = self.env['account.journal'].search([('type','=','bank')])
			if bank_journal_ids:
				journal = bank_journal_ids[0].id
		
		if journal == 'bank':
			bank_journal_ids = self.env['account.journal'].search([('type','=','bank')])
			if bank_journal_ids:
				journal = bank_journal_ids[0].id
						
		values = {
			'name' : self.env['ir.sequence'].with_context(ir_sequence_date=date_now).next_by_code('account.payment.customer.invoice'),
			'payment_type' : "inbound",
			'amount' : wallet,
			'communication' : "Wallet Recharge",
			'payment_date' : datetime.now().date(),
			'journal_id' : journal,
			'payment_method_id': 1,
			'partner_type': 'customer',
			'partner_id': partner.id,
			'description' : descr or '',
		}
		payment_create = account_payment_obj.sudo().create(values)
		payment_create.post() # Confirm Account Payment
				
		total_amount = partner.wallet_balance + float(wallet) # Total Amount
		
		partner.write({'wallet_balance': total_amount })	
					
		return True
		
		
	name = fields.Char('Name', default=lambda self: self.env['ir.sequence'].next_by_code('pos.wallet.transaction'))
	wallet_type = fields.Selection([
		('credit', 'Credit'),
		('debit', 'Debit')
		], string='Type', default='credit')
	partner_id = fields.Many2one('res.partner', 'Customer')
	pos_order_id = fields.Many2one('pos.order', 'POS Order')
	#wallet_id = fields.Many2one('res.partner', 'Wallet')
	reference = fields.Selection([
		('manual', 'Manual'),
		('pos_order', 'POS Order')
		], string='Reference', default='manual')
	amount = fields.Char('Amount')
	currency_id = fields.Many2one('res.currency', 'Currency')
	status = fields.Selection([
		('draft', 'Draft'),
		('done', 'Done')
		], string='Status', readonly=True, default='draft')

				
class WalletRecharge(models.TransientModel):
	_name = 'wallet.recharge'
	_description ='Wallet Recharge' 

	recharge_amount = fields.Float('Recharge Amount',required="True")
	journal_id = fields.Many2one('account.journal', 'Payment Journal',required="True")
	
	def post(self):
		context = self._context
		active_ids = context.get('active_ids')
		account_payment_obj = self.env['account.payment']
		partner_wallet_id = self.env['res.partner'].browse(active_ids[0])
		wallet_transaction_obj = self.env['pos.wallet.transaction']
		
		date_now = datetime.strftime(datetime.now(), '%Y-%m-%d')
		
		vals = {}
		
		vals = {
			'name' : self.env['ir.sequence'].with_context(ir_sequence_date=date_now).next_by_code('account.payment.customer.invoice'),
			'payment_type' : "inbound",
			'amount' : self.recharge_amount,
			'communication' : "Wallet Recharge",
			'payment_date' : datetime.now().date(),
			'journal_id' : self.journal_id.id,
			'payment_method_id': 1,
			'partner_type': 'customer',
			'partner_id': partner_wallet_id.id,
		}
		payment_create = account_payment_obj.sudo().create(vals)
		payment_create.post() # Confirm Account Payment
		value = {
			'wallet_type' : 'credit',
			'reference' : 'manual',
			'amount' : self.recharge_amount,
			'partner_id': partner_wallet_id.id,
			'currency_id' : partner_wallet_id.property_product_pricelist.currency_id.id,
		}
		wallet_obj = wallet_transaction_obj.sudo().create(value)
		
		total_amount = partner_wallet_id.wallet_balance + self.recharge_amount
		
		partner_wallet_id.write({'wallet_balance': total_amount })
		
		return
			   
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
