from odoo import models, fields, api

class ACSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    select_account_whatsapp = fields.Many2one('whatsapp.settings', string="Select Whatsapp Account")
    whatsapp_signature = fields.Boolean('WhatsApp Signature')
    quotation_orders = fields.Boolean(string='Quotation & Order')
    invoices = fields.Boolean(string='Invoices')
    purchase = fields.Boolean(string='Purchase')
    payment = fields.Boolean(string='Payments Receipt')
    inventory = fields.Boolean(string='Inventory')

    @api.model
    def set_values(self):
        super(ACSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        if self.select_account_whatsapp or self.whatsapp_signature:
            param.set_param('whatsapp_dyn.select_account_whatsapp', self.select_account_whatsapp.id)
            param.set_param('whatsapp_dyn.whatsapp_signature', self.whatsapp_signature)
            param.set_param('whatsapp_dyn.quotation_orders', self.quotation_orders)
            param.set_param('whatsapp_dyn.invoices', self.invoices)
            param.set_param('whatsapp_dyn.purchase', self.purchase)
            param.set_param('whatsapp_dyn.payment', self.payment)
            param.set_param('whatsapp_dyn.inventory', self.inventory)
            return param
        else:
            return param

    @api.model
    def get_values(self):
        res = super(ACSettings, self).get_values()
        res.update(
            whatsapp_signature=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.whatsapp_signature') == 'True' else False,
            quotation_orders=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.quotation_orders') == 'True' else False,
            invoices=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.invoices') == 'True' else False,
            purchase=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.purchase') == 'True' else False,
            payment=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.payment') == 'True' else False,
            inventory=True if self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.inventory') == 'True' else False,
            select_account_whatsapp=int(self.env['ir.config_parameter'].sudo().get_param('whatsapp_dyn.select_account_whatsapp')))
        return res
