{
    'name': 'Discount on POS',
    'version': '15.0.1.0.0',
    'depends': ['point_of_sale'],
    'summary': 'Disocunt in POS.',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,

    'depends': ['base', 'point_of_sale'],
    'data': ['views/discount_pos_custom.xml',
             ],

    'assets': {

        'web.assets_backend': [
            'discount_pos_custom/static/src/js/product_screen_button.js',
            'discount_pos_custom/static/src/js/disocunt_pop.js',

        ],
        'web.assets_qweb': [
            'discount_pos_custom/static/src/xml/product_screen_button.xml',
            'discount_pos_custom/static/src/xml/popup.xml',

        ],
      },

}
