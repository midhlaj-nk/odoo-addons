{
    'name': 'Material Request',
    'version': '15.0.1.0.0',
    'summary': 'An application to manage request for product',
    'application': True,
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/material_request.xml',
        'views/material_request_form.xml',

    ],
    'depends': ['base', 'mail', 'account'],

}
