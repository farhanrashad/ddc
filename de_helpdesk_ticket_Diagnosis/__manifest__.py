{

    'name': 'Helpdesk Ticket Diagnosis',
    'description': 'For daily needs data',
    'author': 'Usman',
    'depends':
        [
            'de_helpdesk',
            'mail',
            
            
        ],
    'data':
        [    
           
            'views/bos_custom.xml',
            'security/ir.model.access.csv',
            'data/seq.xml'
        ],
    'installable': True,

}