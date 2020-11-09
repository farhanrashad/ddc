# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        warranty_count = request.env['sales.warranty'].search_count(
            [('partner_id', 'child_of', partner.id)])
        values['warranty_count'] = warranty_count
        return values

    def _helpdesk_warrancy_check_access(self, warranty_id):
        warranty = request.env['sales.warranty'].browse([warranty_id])
        warranty_sudo = warranty.sudo()
        try:
            warranty.check_access_rights('read')
            warranty.check_access_rule('read')
        except AccessError:
            raise
        return warranty_sudo

    @http.route(
        ['/my/warranty', '/my/warranty/page/<int:page>'],
        type='http',
        auth="user",
        website=True,
    )
    def portal_my_warranty(
            self,
            page=1,
            date_begin=None,
            date_end=None,
            sortby=None,
            filterby=None,
            **kw):
        values = self._prepare_portal_layout_values()
        SalesWarranty = request.env['sales.warranty']
        partner = request.env.user.partner_id
        domain = [('partner_id', 'child_of', partner.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'),
                       'order': 'last_stage_update desc'},
        }
        searchbar_filters = {'all': {'label': _('All'), 'domain': []}}
        #for stage in request.env['sales.warranty'].search([]):
            #searchbar_filters.update({
                #str(stage.id): {'label': stage.name,
                                #'domain': [('stage_id', '=', stage.id)]}
            #})

        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        warranty_count = HelpdesTicket.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/warranty",
            url_args={},
            total=ticket_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        warranty = SalesWarranty.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        values.update({
            'date': date_begin,
            'warranty': warranty,
            'page_name': 'ticket',
            'pager': pager,
            'default_url': '/my/tickets',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
        })
        return request.render("de_sale_warranty.portal_my_warranty", values)

    @http.route(['/my/warranty/<int:warranty_id>'], type='http', website=True)
    def portal_my_warranty(self, warranty_id=None, **kw):
        try:
            warranty_sudo = self._sales_warranty_check_access(warranty_id)
        except AccessError:
            return request.redirect('/my')
        values = self._ticket_get_page_view_values(warranty_sudo, **kw)
        return request.render("de_sale_warranty.portal_sales_warranty_page",
                              values)

    def _warramtu_get_page_view_values(self, warranty, **kwargs):
        #closed_stages = request.env['helpdesk.ticket.stage'].search([('closed', '=', True)])
        values = {
            'page_name': 'ticket',
            'warranty': warranty,
            #'closed_stages': closed_stages,
        }

        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):
            values['success'] = kwargs['success']

        return values
