# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class JobOrder(models.Model):
    _name = 'job.order'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Job Order'
    _order = 'date_order desc, id desc'
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    
    struct_id = fields.Many2one('job.order.structure', string='Structure',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Defines the rules that have to be applied to this Job Order, accordingly ')
    
    sale_id = fields.Many2one('sale.order', 'Order Reference',required=False,  readonly=True, states={'draft': [('readonly', False)]},)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('processed', 'Processed'),
        ('done', 'Approved'),
        ('cancel', 'Cancelled')], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    date_order = fields.Datetime(string='Job Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    
    note = fields.Text(string="Note")
    
    job_order_lines = fields.One2many('job.order.line', 'job_order_id', string='Job Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    job_order_routing_ids = fields.One2many('job.order.routing', 'job_order_id', string='Job Order Routings', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    job_order_sale_lines = fields.One2many('job.order.sale.line', 'job_order_id', string='Order Sale Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    job_order_mrp_ids = fields.One2many('job.order.mrp', 'job_order_id', string='Job Order MRP Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    
    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env.company,
        index=True, required=True)
    
    procurement_group_id = fields.Many2one(
        string='Procurement Group',
        comodel_name='procurement.group',
        copy=False)
    routing_id = fields.Many2one(
        comodel_name='mrp.routing', string='Routing',
        on_delete='setnull', readonly=True,
        states={'draft': [('readonly', False)]},
        help="The list of operations (list of work centers) to produce "
             "the finished product. The routing is mainly used to compute "
             "work center costs during operations and to plan future loads "
             "on work centers based on production plannification.")
    
    #details_by_component = fields.One2many('hr.payslip.line',compute='_compute_details_by_salary_rule_category', string='Details by Salary Rule Category')
    
    details_by_category = fields.One2many('job.order.line', compute='_compute_details_by_category', string='Details by Category')
    
    bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', string='Bill of Materials')
    bom_count = fields.Integer(string='BOMs', compute='_compute_bom_ids')
    
    production_ids = fields.One2many('mrp.production', 'job_order_id', string='Productions')
    production_count = fields.Integer(string='Productions', compute='_compute_production_count')
    
    purchase_ids = fields.One2many('purchase.order', 'job_order_id', string='Purchases')
    purchase_count = fields.Integer(string='Subcontract', compute='_compute_subcontract_count')
    
    @api.depends('production_ids')
    def _compute_production_count(self):
        production_data = self.env['mrp.production'].sudo().read_group([('job_order_id', 'in', self.ids)], ['job_order_id'], ['job_order_id'])
        mapped_data = dict([(r['job_order_id'][0], r['job_order_id_count']) for r in production_data])
        for job in self:
            job.production_count = mapped_data.get(job.id, 0)

    def action_view_productions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productions'),
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
            'domain': [('job_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_company_id=self.company_id.id, default_job_order_id=self.id),
        }
    
    @api.depends('purchase_ids')
    def _compute_subcontract_count(self):
        purchase_data = self.env['purchase.order'].sudo().read_group([('job_order_id', 'in', self.ids)], ['job_order_id'], ['job_order_id'])
        mapped_data = dict([(r['job_order_id'][0], r['job_order_id_count']) for r in purchase_data])
        for job in self:
            job.purchase_count = mapped_data.get(job.id, 0)

    def action_view_purchases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchases'),
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('job_order_id', '=', self.id)],
            'context': dict(self._context, create=False, default_company_id=self.company_id.id, default_job_order_id=self.id),
        }
    
    def _compute_production_count(self):
        for job in self:
            job.production_count = self.env['mrp.production'].search_count([('job_order_id', '=', job.id)])
    
    def _compute_details_by_category(self):
        for job in self:
            job.details_by_category = job.mapped('job_order_lines').filtered(lambda line: line.category_id)
            
    @api.depends('bom_ids')
    def _compute_bom_ids(self):
        b = 0
        for order in self:
            for line in order.job_order_lines:
                b = len(line.product_tmpl_id.bom_ids)
            order.bom_count = b
    
    def action_view_bom(self):
        action = self.env.ref('mrp.mrp_bom_tree_view').read()[0]

        boms = self.mapped('boms_ids')
        if len(boms) > 1:
            action['domain'] = [('id', 'in', boms.ids)]
        elif boms:
            action['views'] = [(self.env.ref('mrp.mrp_bom_form_view').id, 'form')]
            action['res_id'] = boms.id
        return action
    
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('job.order') or ' '
        res_id = super(JobOrder, self).create(vals)
        return res_id
    
    def generate_orders(self):
        bom_ids = []
        primary_bom_ids = []
        all_boms = []
        product_id = 0
        var1 = ''
        rule_qty = 0
        
        #self.state = 'processed'
        #finish_production_id = self.env['mrp.production']
        #semi_production_id = self.env['mrp.production']
        for line in self.job_order_sale_lines:
            #bom_ids = self.env['mrp.bom'].browse(line.bom_id).id
            #res = line.sale_line_id._compute_qty_to_deliver()
            fvals = {
                'product_id': line.product_id.id,
                'product_uom_id':line.product_id.uom_id.id,
                'product_qty':line.product_uom_qty,
                'bom_id':line.bom_id.id,
                'origin':self.sale_id.name,
                #'orderpoint_id':self.sale_id.id,
                'job_order_id': self.id,
                'ref_sale_id':self.sale_id.id,
            }
            vals = self._prepare_manufacturing_order(line)
            #mo = self.env['mrp.production'].create(vals)
            #mo._update_raw_move(line.bom_id.id,mo._get_moves_raw_values)
            #finish_production_id.move_raw_ids = [(2, move.id) for move in finish_production_id.move_raw_ids.filtered(lambda m: m.bom_line_id)]
            #finish_production_id.picking_type_id = finish_production_id.bom_id.picking_type_id or finish_production_id.picking_type_id
            #self.env.cr.commit()

            if not (line.bom_id in bom_ids):
                bom_ids.append(line.bom_id)
            
        for boms in bom_ids:
            #var1 = var1 + ',' + p
            #var1 = var1 + '--' + str(boms.id)
            all_boms += boms._recursive_boms()
            #var1 = var1 + ',' + str(all_boms)
            primary_bom_ids.append(boms.id)
            #var1 = str(primary_bom_ids)
        #sub_boms = self.env['mrp.bom'].search([('id', 'in', all_boms ),('id', 'not in', primary_bom_ids )])
        #for bom in sub_boms:
            
            #product_id1 = self.env['product.product'].search([('product_tmpl_id', '=', bom.product_tmpl_id.id )],limit=1)
            #vendor_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', bom.product_tmpl_id.id )]).name
            picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
            
            #self.env.cr.execute('select l.quantity from job_order o join job_order_sale_line s on s.job_order_id = o.id join job_order_line l on l.job_sale_line_id = s.id join job_order_bom b on l.job_rule_id = b.job_rule_id where s.product_tmpl_id=%s ',(bom.product_tmpl_id.id,))

            #for rs in self.env.cr.dictfetchall():
                #rule_qty += rs['quantity']
			#vals = {
			#	'partner_id': 1,
             #   'group_id': self.sale_id.id,
            #    'origin': self.sale_id.name,
            #    'picking_type_id': picking_type_id.id,
            #    'date_order': self.date_order,
            #    'job_order_id': self.id,
            #}
            #purchase_id = self.env['purchase.order'].create(vals)
                        
        for mrp in self.job_order_mrp_ids:
            product_id = self.env['product.product'].search([('product_tmpl_id', '=', mrp.bom_id.product_tmpl_id.id )],limit=1)
            vendor_id = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', mrp.bom_id.product_tmpl_id.id )]).name
            if mrp.bom_id.type == 'normal':
                svals = {
                    'product_id': product_id.id,
                    'product_uom_id':product_id.uom_id.id,
                    'product_qty':mrp.quantity,
                    'bom_id':mrp.bom_id.id,
                    'origin':self.sale_id.name,
                    #'orderpoint_id':self.sale_id.id,
                    'procurement_group_id':self.sale_id.id,
                    'job_order_id': self.id,
                    'ref_sale_id':self.sale_id.id,
                }
                #semi_production_id = self.env['mrp.production'].create(svals)
                #self.env.cr.commit()

            elif mrp.bom_id.type == 'subcontract':
                
                #self.env.cr.commit()
                line_val = {
                    'name':product_id.name,
                    'order_id':purchase_id.id,
                    'product_id':product_id.id,
                    'product_uom':product_id.uom_po_id.id,
                    'product_qty':mrp.quantity,
                    'price_unit':1,
                    'date_planned': self.date_order,
                }
                purchase_line_id = self.env['purchase.order.line'].create(line_val)
                self.env.cr.commit()
       
        #raise Warning(_(rule_qty))
    
    def _prepare_manufacturing_order(self,line):
        self.ensure_one()
        picking_type_id = self.env['stock.picking.type'].browse(self.env['mrp.production']._get_default_picking_type())
        location_src_id = self.env['stock.location'].browse(self.env['mrp.production']._get_default_location_src_id())
        location_dest_id = self.env['stock.location'].browse(self.env['mrp.production']._get_default_location_dest_id())
        return {
            'product_id': line.product_id.id,
            'bom_id': line.bom_id.id,
            'product_qty': line.product_uom_qty,
            'product_uom_id': line.product_id.uom_id.id,
            'job_order_id': self.id,
            'origin': self.sale_id.name,
            'location_src_id': location_src_id.id,
            'location_dest_id': location_dest_id.id,
            'picking_type_id': picking_type_id.id,
            'routing_id': self.routing_id.id,
            'date_planned_start': self.date_order,
            'date_planned_finished': self.date_order,
            'procurement_group_id': self.procurement_group_id.id,
            #'propagate': self.propagate,
            'company_id': self.company_id.id,
        }
    
    def _prepare_bom(self, product_template, product, type, quantity, contractors):
        return {
            'product_tmpl_id':product_template.id,
            'product_id':product.id,
            'product_uom_id':product_template.uom_id.id,
            'product_qty':quantity,
            'type':type,
            'subcontractor_ids':[( 6, 0, contractors)],
        }
    def _prepare_bom1(self, product_template, type, quantity, contractors):
        return {
            'product_tmpl_id':product_template.id,
            'product_uom_id':product_template.uom_id.id,
            'product_qty':quantity,
            'type':type,
            'subcontractor_ids':[( 6, 0, contractors)],
        }
    
    def _prepare_bom_line(self, bom, product, quantity):
        return {
            'bom_id': bom.id,
            'product_id':product.id,
            'product_qty':quantity
        }
    def _prepare_reorder(self, product, location):
        return {
            'product_id':product.id,
            'product_min_qty':0,
            'product_max_qty':0,
            'qty_multiple':1,
            'location_id':location,
        }
    def _prepare_product(self, name, category, product_template, weight):
        return {
            'name': name,
            'type':product_template.type,
            'categ_id':category.id,
            'sale_ok':False,
            'purchase_ok':True,
            'uom_id':product_template.uom_id.id,
            'uom_po_id':product_template.uom_po_id.id,
            'route_ids':  [],
            'ref_product_tmpl_id': product_template.id,
            #'ref_product_id': rs.product_id.id,
            'tracking':'lot',
            'weight':weight,  
        }
    
    #def _prepare_vendor_pricelist(self,partner_id, product_template):
        #return {
          #  'name':partner_id.id,
         #   'min_qty':1,
         #   'price':1,
         #   'product_tmpl_id':product_template.id,
         #   'is_subcontractor':True,
       # }        
                
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def action_draft(self):
        self.state = 'draft'
    
    def action_update_so_in_product(self):
        #update reference in all MO
        #for bom in self.job_order_sale_lines:
        productions = self.env['mrp.production'].search(['|',('ref_sale_id','=',self.sale_id.id),('job_order_id','=',self.id)])
        pickings = self.env['stock.picking'].search(['|',('ref_sale_id','=',self.sale_id.id),('job_order_id','=',self.id)])
        
        for production in productions:
            for finish_move_line in production.finished_move_line_ids:
                finish_move_line.update({
                    'job_order_id': self.id,
                    'sale_id':self.sale_id.id,
                })
            for finish_move in production.move_finished_ids:
                finish_move.update({
                    'job_order_id': self.id,
                    'sale_id':self.sale_id.id,
                })
            for raw_move in production.move_raw_ids:
                raw_move.update({
                    'job_order_id':self.id,
                    'sale_id':self.sale_id.id,
                })
                for raw_move_line in raw_move.move_line_ids:
                    raw_move_line.update({
                        'job_order_id':self.id,
                        'sale_id':self.sale_id.id,
                    })
        
        for picking in pickings:
            for move in picking.move_lines:
                move.update({
                    'job_order_id':self.id,
                    'sale_id':self.sale_id.id,
                })
            for move_line in picking.move_line_ids:
                move_line.update({
                    'job_order_id':self.id,
                    'sale_id':self.sale_id.id,
                })
        ref_moves = self.env['stock.move'].search(['|',('ref_sale_id','=',self.sale_id.id),('ref_job_order_id','=',self.id)])
        for move in ref_moves:
            move.update({
                'job_order_id': move.ref_job_order_id.id,
                'sale_id': move.ref_sale_id.id,
            })
            
        ref_move_lines = self.env['stock.move.line'].search(['|',('ref_sale_id','=',self.sale_id.id),('ref_job_order_id','=',self.id)])
        for line in ref_move_lines:
            line.update({
                'job_order_id': line.ref_job_order_id.id,
                'sale_id': line.ref_sale_id.id,
            })
        #update product for components
        for cline in self.job_order_mrp_ids:
            for product in cline.bom_id.product_tmpl_id:
                for variant in product.product_variant_ids:
                    variant.update({
                        'sale_id': self.sale_id.id
                    })
                product.update({
                    'sale_id': self.sale_id.id
                })
                
                
        for sline in self.job_order_sale_lines:
            for product in sline.bom_id.product_tmpl_id:
                product.update({
                    'sale_id': self.sale_id.id,
                })
                for variant in product.product_variant_ids:
                    variant.update({
                        'sale_id': self.sale_id.id,
                    })
                for c_variant in sline.bom_id.bom_line_ids.product_id:
                    for c_product in c_variant.product_tmpl_id:
                        c_product.update({
                            'sale_id': self.sale_id.id,
                        })
                    c_variant.update({
                        'sale_id': self.sale_id.id,
                    })
    def action_process(self):
        bom_ids = []
        all_boms = []
        self.job_order_lines.unlink()
        self.job_order_mrp_ids.unlink()
        job_order_line = self.env['job.order.line']
        for job in self:
            for sale in job.job_order_sale_lines:
                if not (sale.bom_id in bom_ids):
                    bom_ids.append(sale.bom_id)
                #sale = sale.id
                for rule in job.struct_id.rule_ids:
                    result_dict = {
                        'job_order_id':job.id,
                        'job_sale_line_id':sale.id,
                        'name': sale.product_tmpl_id.name + '-' + rule.name,
                        'code':rule.code,
                        'sequence':rule.sequence,
                        'category_id':rule.category_id.id,
                        'job_rule_id':rule.id,
                        'line_desc':rule.name,
                        'quantity':sale.product_uom_qty,
                    }
                    job_order_line.create(result_dict)
        
        for boms in bom_ids:
            all_boms += boms._recursive_boms()
        
        bom_line = self.env['job.order.mrp']
        #bom_line = self.env['job.order.mrp'].search([('bom_id', 'not in', [bom_ids])])
        for bom in all_boms:
            val = {
                'job_order_id':self.id,
                'bom_id':bom,
            }
            bom_line.create(val)
         
        for b in bom_ids:
            bom_line.search([('bom_id', '=', b.id)]).unlink()
        
        routings = self.env['mrp.routing'].search([('active', '=', True)])
        #routings = self.env['mrp.routing']
        seq = 0
        self.job_order_routing_ids.unlink()
        job_routing_id = self.env['job.order.routing']
        for g in routings:
            seq += 10
            rvals = {
                'job_order_id':self.id,
                'routing_id':g.id,
                'sequence':seq,
                #'routing_include':True,
            }
            job_routing_id.create(rvals)
        self.env.cr.commit()
        self.state = 'processed'
    
    def action_approve(self):
        self.state = 'done'
        
    def action_confirm(self):
        vals = {}
        self.job_order_sale_lines.unlink()
        job_sale_line = self.env['job.order.sale.line']
        bom = self.env['mrp.bom']
        for line in self.sale_id.order_line:
            bom = self.env['mrp.bom'].search([('product_tmpl_id', '=',line.product_id.product_tmpl_id.id),('product_id', '=',line.product_id.id)],limit=1)
            if line.product_uom_qty:
                vals = {
                    'job_order_id': self.id,
                    'product_tmpl_id': line.product_id.product_tmpl_id.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty' : line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'sale_line_id': line.id,
                    'struct_id': self.struct_id.id,
                    #'bom_id': self._get_bom_id(line.product_id.product_tmpl_id),
                    #'bom_id': line.product_id.product_tmpl_id.bom_ids.id,
                    'bom_id': bom.id
                }
                job_sale_line.create(vals)
                
        self.state = 'confirmed'
    
    def _compute_details_by_component_category(self):
        for job in self:
            job.details_by_component_category = job.mapped('job_order_lines').filtered(lambda line: line.category_id)
    
class JobOrderSaleLine(models.Model):
    _name = 'job.order.sale.line'
    _description = 'Job Order Sale Line'
    _order = 'id desc'
    
    @api.model
    def _get_default_uom(self):
        return self.product_tmpl_id.uom_id
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    
    sale_line_id = fields.Many2one('sale.order.line', string='Order Line', required=True, index=True, ondelete='cascade')
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product',
        domain="[('type', 'in', ['product', 'consu'])]", required=False)
    product_id = fields.Many2one(
        'product.product', 'Product Variant',
        domain="['&', ('product_tmpl_id', '=', product_tmpl_id), ('type', 'in', ['product', 'consu'])]",
        help="If a product variant is defined the BOM is available only for this product.")
    
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',change_default=True, default=_get_default_uom)
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    struct_id = fields.Many2one('job.order.structure', string='Structure', readonly=True)
    bom_id = fields.Many2one('mrp.bom', string='BOM')
    
class JobOrderLine(models.Model):
    _name = 'job.order.line'
    _inherit = 'job.order.rule'
    _description = 'Job Order Line'
    _order = 'sequence'
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    job_sale_line_id = fields.Many2one('job.order.sale.line', string='Job Order Sale Line', index=True, required=True, ondelete='cascade')
    #product_tmpl_id = fields.
    product_tmpl_id = fields.Many2one('product.template', related='job_sale_line_id.product_tmpl_id', string='Product', store=True, readonly=True)
    
    job_rule_id = fields.Many2one('job.order.rule', 'Job Rule',required=True)
    line_desc = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'), default=1.0)
    
    total = fields.Float(compute='_compute_total', string='Total', store=True)

    @api.depends('quantity')
    def _compute_total(self):
        for line in self:
            line.total = float(line.quantity)
            
class JobOrderBOM(models.Model):
    _name = 'job.order.mrp'
    _description = 'Jor Order Production'
    
    #job_order_id = fields.Many2one('Job.order', string='Job Order Reference', required=True, ondelete='cascade', index=True, copy=False, readonly=True)
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    bom_id = fields.Many2one('mrp.bom', string='BOM',readonly=True)
    bom_type = fields.Selection('mrp.bom', related='bom_id.type',string='Type',readonly=True, store=True)
    quantity = fields.Float(string='Quantity',digits=dp.get_precision('Product Unit of Measure'),default=1.0)
    production_quantity = fields.Float(string='Production Quantity', compute='_calcualte_production_quantity', store=False)
    
    def _calcualte_production_quantity(self):
        self.production_quantity = 0
    
    
    
    #@api.depends('job_rule_id')
    def _compute_quantity(self):
        
        test = '0'
        #job_sale_lines = self.env['job.order.sale.line'].search([('job_order_id', '=', rs.job_order_id.id),('product_tmpl_id', '=', line.product_tmpl_id.id)])

        for rs in self:
            rule_qty = 0
            job_order_lines = self.env['job.order.line'].search([('job_order_id', '=', rs.job_order_id.id),('job_rule_id', '=', rs.job_rule_id.id)])
            for line in job_order_lines:
                rule_qty += line.quantity
                #for sale in job_sale_lines:
                    #rule_qty += line.quantity
                    #if line.job_rule_id.id == rs.job_rule_id.id:
                        #if sale.product_tmpl_id.id == line.job_sale_line_id.product_tmpl_id.id:
                            #rule_qty += line.quantity
                        #rule_qty += 0
                            #rule_qty += line.quantity
            rs.quantity = rule_qty
        #raise Warning(_(self.bom_id.product_tmpl_id.id))
        
class JobOrderRouting(models.Model):
    _name = 'job.order.routing'
    _description = 'Job Order Routing'
    _order = 'sequence'
    
    job_order_id = fields.Many2one('job.order', string='Order Reference', index=True, required=True, ondelete='cascade')
    routing_id = fields.Many2one('mrp.routing', string='Routing')
    sequence = fields.Integer(string='Sequence', required=True, default=10)
    routing_include = fields.Boolean('Include',default=True)
    is_subcontracting = fields.Boolean('Is Subcontracting',default=True)
    apply_on_variant = fields.Boolean('Apply on variant',default=True)
    
    