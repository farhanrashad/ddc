# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountPaymentExt(models.Model):
    _inherit = 'account.payment'

    def action_transfer_in(self):
        self.state = 'cash_sent'
        

    def action_transfer_out(self):
        self.state = 'cash_received'
        self.state = 'draft'
        self.post()

    def get_internal_transactions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Transactions',
            'target': 'current',
            'res_model': 'internal.transaction',
            'domain': [('user_id', '=', self.env.user.id)],
            'view_mode': 'tree,form',
        }

    def _get_total_transactions(self):
        for record in self:
            record.transaction_count = self.env['internal.transaction'].search_count(
                [('user_id', '=', self.env.user.id)])

    def _get_current_user(self):
        for rec in self:
            rec.current_user_id = self.env.user

    @api.depends('cash_issue_user_id')
    def _compute_current_issue(self):
        print('No')
        if self.cash_issue_user_id == self.env.user:
            print('yes')
            self.is_current_issue = True
        else:
            self.is_current_issue = False

    @api.depends('cash_receive_user_id')
    def _compute_current_receive(self):
        if self.cash_receive_user_id == self.env.user:
            self.is_current_receive = True
        else:
            self.is_current_receive = False

    @api.depends('cash_issue_user_id','current_user_id','state')
    def _get_transfer_status(self):
        for rs in self:
            if rs.branch_transfer and rs.state == 'draft' and rs.current_user_id.id == rs.cash_issue_user_id.id:
                rs.transfer_status = 'i'
            elif rs.branch_transfer and rs.state == 'cash_sent' and rs.current_user_id.id == rs.cash_receive_user_id.id:
                rs.transfer_status = 'r'
            elif not(rs.branch_transfer) and rs.state == 'draft':
                rs.transfer_status = 'd'
            else:
                rs.transfer_status = 'n'
        
    branch_transfer = fields.Boolean(string='Branch Transfer')
    cash_issue_user_id = fields.Many2one('res.users', string='Cash Issue User',
                                         related='journal_id.user_id')
    cash_receive_user_id = fields.Many2one('res.users', string='Cash Receive User',
                                           related='destination_journal_id.user_id')
    current_user_id = fields.Many2one('res.users', compute='_get_current_user')
    
    state = fields.Selection([('draft', 'Draft'), ('cash_sent', 'Cash Send'),('cash_received', 'Cash Received'),('posted', 'Validated'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], readonly=True, default='draft', copy=False, string="Status")
    transfer_status = fields.Char(string='Transfer Status', compute='_get_transfer_status')
    #transfer_in = fields.Boolean(string='Transfer In')
    #transfer_out = fields.Boolean(string='Transfer Out')
    #transaction_count = fields.Integer(compute='_get_total_transactions')
    #current_user = fields.Many2one(comodel_name='res.users', compute='_get_current_user')
    #is_current_issue = fields.Boolean(string='Current Issue', compute='_compute_current_issue')
    #is_current_receive = fields.Boolean(string='Current Receive', compute='_compute_current_receive')


class AccountJournalExt(models.Model):
    _inherit = 'account.journal'

    user_id = fields.Many2one(comodel_name='res.users', string='User')
    #cash_issue_user_id = fields.Many2one(comodel_name='res.users', string='Cash Issue User')
    #cash_receive_user_id = fields.Many2one(comodel_name='res.users', string='Cash Receive User')
