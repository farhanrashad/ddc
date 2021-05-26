{

    'name': 'Invoice Commissions',
    'summary': 'Invoice Commissions for Sales',
    'author': 'Dynexcel',
    'depends':
        [
            'base','hr', 'sale', 'contacts', 'account_accountant', 'sale_management'
        ],
    'data':
        [
            'data/invoice_server_action.xml',
            'security/ir.model.access.csv',
            'views/invoice_commission_views.xml',
        ],
    'installable': True,

}