# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket", help="Related Helpdesk Ticket")
    is_diagnosys = fields.Boolean('Is Diagnosys')
    is_workorder = fields.Boolean('Is Workorder')
    is_repair_sale = fields.Boolean('Repair Sale',default=False)
    closed = fields.Boolean(related='ticket_id.closed',string='Closed')
    
    repair_planning_lines = fields.One2many("project.task.planning.line", "task_id", string="Task Repair Planning Lines", readonly=False, attr="{'readonly':[('closed','=',True)]}", copy=True, auto_join=True)
    
    sale_amount_total = fields.Float(compute='_compute_sale_data', string="Sum of Orders", help="Untaxed Total of Confirmed Orders", )
    quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    sale_order_count = fields.Integer(compute='_compute_sale_data', string="Number of Sale Orders")
    order_ids = fields.One2many('sale.order', 'repair_task_id', string='Orders')
    
    remarks = fields.Html(string='Technician Remarks')
    
    
    @api.depends('order_ids.state', 'order_ids.currency_id', 'order_ids.amount_untaxed', 'order_ids.date_order', 'order_ids.company_id')
    def _compute_sale_data(self):
        for task in self:
            total = 0.0
            quotation_cnt = 0
            sale_order_cnt = 0
            company_currency = self.env.company.currency_id
            for order in task.order_ids:
                if order.state in ('draft', 'sent'):
                    quotation_cnt += 1
                if order.state not in ('draft', 'sent', 'cancel'):
                    sale_order_cnt += 1
                    total += order.currency_id._convert(
                        order.amount_untaxed, company_currency, order.company_id, order.date_order or fields.Date.today())
            task.sale_amount_total = total
            task.quotation_count = quotation_cnt
            task.sale_order_count = sale_order_cnt
    
    def action_view_sale_quotation(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_repair_task_id': self.id
        }
        action['domain'] = [('repair_task_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('order_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_view_sale_order(self):
        action = self.env.ref('sale.action_orders').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_repair_task_id': self.id,
        }
        action['domain'] = [('repair_task_id', '=', self.id), ('state', 'not in', ('draft', 'sent', 'cancel'))]
        orders = self.mapped('order_ids').filtered(lambda l: l.state not in ('draft', 'sent', 'cancel'))
        if len(orders) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = orders.id
        return action
    
    

    def action_view_so(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            'name': _('Sale Order'),
            #"views": [[False, "form"]],
            'view_mode': 'tree,form',
            "res_id": self.sale_order_id.id,
            "context": {"create": False, "show_sale": True},
        }
            
    def action_create_sale_order(self):
        self.ensure_one()
        #res = self.env['sale.order'].browse(self._context.get('id',[]))
        res = self.env['sale.order']
        lines_data = []
        pricelist = self.partner_id.property_product_pricelist
        partner_pricelist = self.partner_id.property_product_pricelist
        
        for line in self.repair_planning_lines:
            lines_data.append([0,0,{
                'product_id' : line.product_id.id,
                'name' : line.name,
                'product_uom_qty' : line.product_uom_qty,
                'product_uom' : line.product_uom_id.id,
				'price_unit' : line.price_unit,
                'project_id': self.project_id.id,  # prevent to re-create a project on confirmation
                'task_id': self.id,
                'repair_planning_line_id': line.id,
            }])
        
        res.create({
            'project_id': self.project_id.id,
            'partner_id' : self.partner_id.id,
            'analytic_account_id': self.project_id.analytic_account_id.id,
            'client_order_ref': self.project_id.name,
            'company_id': self.project_id.company_id.id,
            'repair_task_id':self.id,
            'ticket_id': self.ticket_id.id,
            'order_line':lines_data,
        })
        self.update({
            'is_repair_sale':True,
        })
        return res
    
    
class ProjectTaskRepairPlanning(models.Model):
    _name = 'project.task.planning.line'
    _description = 'Repair Planning Line'
    _order = 'id desc'
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    task_id = fields.Many2one('project.task', string='Task', index=True, required=True, ondelete='cascade')
    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True,)
    product_uom_qty = fields.Float('Quantity', default=1.0, required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_product_uom_id, required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    
    invoice_amount = fields.Float(string='Invoiced Amount', compute='_get_invoice_amount')
    qty_delivered = fields.Float(string='Delivered Quantity', compute='_compute_qty_delivered')

    @api.depends('product_uom_qty')
    def _compute_qty_delivered(self):
        order_line_id = self.env['sale.order.line']
        qty = 0
        for line in self:
            qty = 0
            if line.product_id.type == 'product':
                order_line_id = self.env['sale.order.line'].search(             
                    [('repair_planning_line_id','=',line.id)],limit=1)
                for qline in order_line_id:
                    qty = qline.qty_delivered
            line.qty_delivered = qty

    @api.depends('product_uom_qty', 'price_unit')
    def _get_invoice_amount(self):
        order_line_id = self.env['sale.order.line']
        amt = 0
        for line in self:
            amt = 0
            order_line_id = self.env['sale.order.line'].search([('repair_planning_line_id','=',line.id)])
            for invoice_line in order_line_id.invoice_lines:
                if invoice_line.move_id.state != 'cancel':
                    if invoice_line.move_id.type == 'out_invoice':
                        amt += invoice_line.price_total
                    elif invoice_line.move_id.type == 'out_refund':
                        amt -= invoice_line.price_total
            line.invoice_amount = amt
    
    @api.onchange('task_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        """ On change of product it sets product quantity, tax account, name,
        uom of product, unit price and price subtotal. """
        if not self.product_id:
            return
        pricelist = self.task_id.partner_id.property_product_pricelist
        partner = self.task_id.partner_id

        if partner and self.product_id:
            fp = partner.property_account_position_id
            if not fp:
                # Check automatic detection
                fp_id = self.env['account.fiscal.position'].get_fiscal_position(partner.id, delivery_id=self.task_id.partner_id.id)
                fp = self.env['account.fiscal.position'].browse(fp_id)
            self.tax_id = fp.map_tax(self.product_id.taxes_id, self.product_id, partner).ids
        if self.product_id:
            self.name = self.product_id.display_name
            self.product_uom_id = self.product_id.uom_id.id
            if self.product_id.description_sale:
                self.name += '\n' + self.product_id.description_sale
                
        if not pricelist:
            self.price_unit = self.product_id.lst_price
        else:
            self._onchange_product_uom()
                
    @api.onchange('product_uom_id')
    def _onchange_product_uom(self):
        partner = self.task_id.partner_id
        pricelist = self.task_id.partner_id.property_product_pricelist
        if pricelist and self.product_id:
            price = pricelist.get_product_price(self.product_id, self.product_uom_qty, partner, uom_id=self.product_uom_id.id)
            if price is False:
                warning = {
                    'title': _('No valid pricelist line found.'),
                    'message':
                        _("Couldn't find a pricelist line matching this product and quantity.\nYou have to change either the product, the quantity or the pricelist.")}
                return {'warning': warning}
            else:
                self.price_unit = price