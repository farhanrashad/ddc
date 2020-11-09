from odoo import fields, models, api, _

   
class helpdesk_customized(models.Model):
    _inherit = 'helpdesk.ticket'
    
    fault= fields.Html('Fault/Diagnosys')
    
    remarks = fields.Html('Remarks')


    
                
            