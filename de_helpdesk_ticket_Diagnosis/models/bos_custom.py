from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning
from datetime import datetime

   
class helpdesk_custom(models.Model):
    _inherit = 'helpdesk.ticket'
    

    
    boc_count = fields.Integer(string="Diagnosis", compute='_get_calculate', readonly=True)

    
    def _get_calculate(self):
        for order in self:
            bos = self.env['helpdesk.ticket.diagnosys'].search([('ticket_id', '=', self.id) ])

            order.boc_count = len(bos)
    
    def open_ticket(self):   
        po = self.env['helpdesk.ticket.diagnosys'].search([('ticket_id', '=', self.id) ])
        action = self.env.ref('de_helpdesk_ticket_Diagnosis.open_internalprocessing_order').read()[0]
        action['context'] = {
        'domain':[('id','in',po.ids)]
        
        }
        action['domain'] = [('id', 'in', po.ids)]
        return action    
    
    
    def button_validated_fault(self):
        lines = self.env['helpdesk.ticket.diagnosys']
        
        line = []
        line =self.env['helpdesk.ticket.diagnosys'].create({'ticket_id': self.id})
            
        return {
            'name': 'wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': line.id,
            'res_model': 'helpdesk.ticket.diagnosys',
            
            }
        

class internal_MenuForm(models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _name='helpdesk.ticket.diagnosys'
    _description="Helpdesk Ticket Diagnosys"
    
    
    date_to=fields.Date("Date", default=datetime.today())
        
    user_id=fields.Many2one('res.users','Responsible',  default=lambda self: self.env.user)
    

    
    name= fields.Char('Name', readonly=True, copy=False,)
    
    fault= fields.Html('Fault/Diagnosys')
    
    remarks = fields.Html('Remarks')


    ticket_id=fields.Many2one('helpdesk.ticket',string="Ticket")
    
                
            
    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == False:
            sequence = self.env.ref('de_helpdesk_ticket_Diagnosis.name')
            vals['name'] = sequence.next_by_id()
        return super(internal_MenuForm, self).create(vals)
    