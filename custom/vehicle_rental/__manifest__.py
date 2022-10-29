{
    'name': 'Vehicle Rental',
    'version': '15.0.1.0.0',
    'depends': ['fleet', 'base', 'mail', 'account' , 'website'],
    'summary': 'An odoo application to manage rental vehicles',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_rental.xml',
        'views/vehicle_rental_tree.xml',
        'views/vehicle_rental_search.xml',
        'views/fleet_inherit.xml',
        'views/vehicle_rental_form.xml',
        'views/rental_request_form.xml',
        'views/vehicle_rental_kanban.xml',
        'views/rental_request_tree.xml',
        'views/website.xml',

        'data/automate.xml',

        'reporting/vehicle_rental_report.xml',
        'reporting/templates.xml',

    ],


    'assets': {
        'web.assets_backend': [
            'vehicle_rental/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'vehicle_rental/static/src/js/main.js',
        ],

    },

}
