{
    'name': 'QR Code Generator',
    'version': '15.0.1.0.0',
    'depends': ['base'],
    'summary': 'QR Code Generator',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,

    'data': ['security/ir.model.access.csv',
        'view/qr_generator_form.xml',
             'view/templates.xml'
             ],

    'assets': {
        'web.assets_backend': {
            '/qr_generator/static/src/js/qr_generator.js',
        },
        'web.assets_qweb': {
            '/qr_generator/static/src/xml/qr_generator.xml',
        },
    },

}
