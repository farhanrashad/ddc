from odoo import models, fields, api, _

class ResPartnercategory(models.Model):
    _inherit = 'account.move'

    tag_id= fields.Many2many(related='partner_id.category_id',readonly=True, string='Tags')