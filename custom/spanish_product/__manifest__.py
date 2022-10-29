{
    'name': 'Spanish Product Name',
    'version': '15.0.1.0.0',
    'depends': ['website', 'point_of_sale'],
    'summary': 'Spanish Product name in POS.',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,

    'depends': ['base', 'website'],
    'data': ['views/pos.xml',
             ],

        'assets': {
            'web.assets_qweb': [
                'spanish_product/static/src/xml/pos_spanish_name.xml',
            ],
            'web.assets_backend': [
                'spanish_product/static/src/js/pos_spanish_name.js',
            ],
        },

}
