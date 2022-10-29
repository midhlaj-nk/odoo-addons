{
    'name': 'Sale order Approvals',
    'version': '15.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'summary': 'Sale order approvals (25k)',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,


'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'views/spotter_sale_order_approval.xml',

    ],
}
