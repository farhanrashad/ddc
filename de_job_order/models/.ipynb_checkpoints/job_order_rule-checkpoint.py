# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class JobOrderStructure(models.Model):
    """
    Job Order structure used to defined
    - Finished
    - Semi Finished
    - Raw Material
    - Utilities
    """
    _name = 'job.order.structure'
    _description = 'Job Order Structure'
    
    name = fields.Char(required=True)
    code = fields.Char(string='Reference', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        copy=False, default=lambda self: self.env['res.company']._company_default_get())
    note = fields.Text(string='Description')
    rule_ids = fields.Many2many('job.order.rule', 'job_structure_job_rule_rel', 'struct_id', 'rule_id', string='Job Order Rules')
    
    def get_all_rules(self):
        """
        @return: returns a list of tuple (id, sequence) of rules that are maybe to apply
        """
        all_rules = []
        for struct in self:
            all_rules += struct.rule_ids.id
        return all_rules
    
    
class JobOrderRuleCategory(models.Model):
    _name = 'job.order.rule.category'
    _description = 'Job Order Rule Category'

    name = fields.Char(required=True, translate=True)    
    

class JobOrderRule(models.Model):
    _name = 'job.order.rule'
    _order = 'sequence, id'
    _description = 'Job Order Rule'
    
    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True,
        help="The code of salary rules can be used as reference in computation of other rules. "
             "In that case, it is case sensitive.")
    sequence = fields.Integer(required=True, index=True, default=5,
        help='Use to arrange calculation sequence')
    category_id = fields.Many2one('job.order.rule.category', string='Category', required=True)
    appears_on_sheet = fields.Boolean(string='Appears on sheet', default=True, help="Used to display the rule on Job Order Sheet.")
    is_total = fields.Boolean(string='total', default=True, help="Used to display total")
    rule_type = fields.Selection([
        ('normal', 'Normal'),
        ('summary', 'Summary'),
        ], string='Rule Type', required=True, default='normal')
    
    active = fields.Boolean(default=True, help="If the active field is set to false, it will allow you to hide the rule without removing it.")
    quantity_select = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fix', 'Fixed Quantity'),
        ('code', 'Python Code'),
    ], string='Quantity Type', index=True, required=True, default='fix', help="The computation method for the rule quantity.")
    quantity_fix = fields.Float(string='Fixed quantity', digits=dp.get_precision('Product Unit of Measure'))
    quantity_percentage = fields.Float(string='Percentage (%)', help='For example, enter 50.0 to apply a percentage of 50%')
    quantity_python_compute = fields.Text(string='Python Code', default="result = 0")
    quantity_percentage_base = fields.Char(string='Percentage based on', help='result will be affected to a variable')
            
    #TODO should add some checks on the type of result (should be float)
    def _compute_rule(self, localdict):
        """
        :param localdict: dictionary containing the environement in which to compute the rule
        :return: returns a tuple build as the base/amount computed, the quantity and the rate
        :rtype: (float, float, float)
        """
        self.ensure_one()
        if self.quantity_select == 'fix':
            try:
                return self.quantity_fix
            except:
                raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (self.name, self.code))
        elif self.quantity_select == 'percentage':
            try:
                return (float(safe_eval(self.quantity_percentage_base, localdict)))
            except:
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s).') % (self.name, self.code))
        else:
            try:
                safe_eval(self.amount_python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0
            except:
                raise UserError(_('Wrong python code defined for salary rule %s (%s).') % (self.name, self.code))
                
                
    def _compute_rule(self, localdict):
        """
        :param localdict: dictionary containing the environement in which to compute the rule
        :return: returns a tuple build as the base/amount computed, the quantity and the rate
        :rtype: (float, float, float)
        """
        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix, float(safe_eval(self.quantity, localdict)), 100.0
            except:
                raise UserError(_('Wrong quantity defined for salary rule %s (%s).') % (self.name, self.code))
        elif self.amount_select == 'percentage':
            try:
                return (float(safe_eval(self.amount_percentage_base, localdict)),
                        float(safe_eval(self.quantity, localdict)),
                        self.amount_percentage)
            except:
                raise UserError(_('Wrong percentage base or quantity defined for salary rule %s (%s).') % (self.name, self.code))
        else:
            try:
                safe_eval(self.amount_python_compute, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), 'result_qty' in localdict and localdict['result_qty'] or 1.0, 'result_rate' in localdict and localdict['result_rate'] or 100.0
            except:
                raise UserError(_('Wrong python code defined for salary rule %s (%s).') % (self.name, self.code))