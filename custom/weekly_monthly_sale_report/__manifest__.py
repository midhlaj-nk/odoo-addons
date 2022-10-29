{
    'name': 'Weekly Monthly Sale reporting',
    'version': '15.0.1.0.0',
    'depends': ['base', 'mail','sale_management'],
    'summary': 'weekly monthly reporting',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,
    #
    'data': [
        'security/ir.model.access.csv',

        'reporting/templates.xml',
        'reporting/reporting.xml',

    ],


    # 'assets': {
    #     'web.assets_backend': [
    #         'vehicle_rental/static/src/js/action_manager.js',
    #     ],
    #     'web.assets_frontend': [
    #         'vehicle_rental/static/src/js/main.js',
    #     ],
    #
    # },

}
