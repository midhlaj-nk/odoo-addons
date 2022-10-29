# -*- coding: utf-8 -*-

{
    'name': 'Customer Route Management',
    'version': '15.0.1.0.0',
    'author': 'Midhlaj Nechikkandan',
    'summary': 'Manage customers in locations',
    'description': "Odoo 15 Customer Route Management v15",
    'depends': [
        'base', 'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
        'reporting/templates.xml',
        'views/delivery_route.xml',
        'views/delivery_route_form.xml',
        'views/delivery_route_inherit.xml'

    ],

    'assets': {
        'web.assets_backend': [
            'customer_route_management/static/src/js/action_manager.js',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
