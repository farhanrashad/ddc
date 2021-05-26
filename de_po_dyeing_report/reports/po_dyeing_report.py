
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re

class PurchaseOrderInherit(models.Model):
    _inherit= 'purchase.order'
    
    def print_po_dyeing_report(self):
        data = {}
        data['form'] = self.read(['id','state'])[0]
        return self.env.ref('de_po_dyeing_report.action_po_dyeing_report').report_action(self, data=data, config=False)

    
class DyeingReport(models.AbstractModel):
    _name = 'report.de_po_dyeing_report.po_dyeing_template'
    
    def get_qty(self, color, model):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        records_list = []
        for record in docs.order_line:
            if record.display_type != "line_section":
                data = record.product_id.name
                x = re.search(model, data)
                y = re.search(color, data)
                if x and y:
                    records_list.append(record.id)
        rec = self.env['purchase.order.line'].browse(records_list)
        if rec:
            rec = rec[0]
            return rec.product_qty
        else:
            return 0.0
        
    def get_weight(self, color, model):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        records_list = []
        for record in docs.order_line:
            if record.display_type != "line_section":
                data = record.product_id.name
                x = re.search(model, data)
                y = re.search(color, data)
                if x and y:
                    records_list.append(record.id)
        rec = self.env['purchase.order.line'].browse(records_list)
        if rec:
            return rec.total_weight
        else:
            return 0.0
    
    def get_weight_unit(self, model):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        records_list = []
#         raise UserError((model))
        for record in docs.order_line:
            if record.display_type != "line_section":
                data = record.product_id.name
                x = re.search(model, data)
#                 y = re.search(color, data)
                if x:
                    records_list.append(record.id)
#         raise UserError((records_list[0]))
        rec = self.env['purchase.order.line'].browse(records_list[0])
#         raise UserError(("Rec " +rec))
#         raise UserError((rec))
        if rec:
            return rec.weight
        else:
            return 0.0
        
        
        
    
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        colors = ''
        description = ''
        color_list = []
        model_list = []
        for record in docs.order_line:
            data = record.product_id.name
            if record.display_type != "line_section":
                color_name = data.split('(', 1)[1].split(')')[0]
                model_name = data.split('(', 1)[0]
                color_list.append(color_name)
                model_list.append(model_name)
#             raise UserError((colors))
#             raise UserError((description))
#             color = colors.find("(")+1:colors.find(")")
        
        color_list = list(dict.fromkeys(color_list))
        model_list = list(dict.fromkeys(model_list))
#         raise UserError((model_list))
        return {
                'docs': docs,
#                 'orders': invoices,
                'model_list':model_list,
                'color_list': color_list,
                'product_qty': self.get_qty,
                'product_weight': self.get_weight,
                'product_unit': self.get_weight_unit
            }