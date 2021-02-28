from odoo import fields, models, api, _

   
class helpdesk_solution(models.Model):
    _inherit = 'helpdesk.ticket.stage'
    
    user_ids= fields.Many2one('res.users',String="Responsible")


class de_helpdesk_solution(models.Model):
    _inherit = 'helpdesk.ticket'
    
    user_id = fields.Many2one('res.users', string='Assigned to' ,compute="usman")
    
    @api.onchange('stage_id')
    @api.depends('name','stage_id')
    def usman(self):
        for ss in self:
            stg =self.env['helpdesk.ticket.stage'].search([])
            if stg:
                for s in stg:
                    if s.name==ss.stage_id.name:
                        ss.user_id= s.user_ids.id
                    
            