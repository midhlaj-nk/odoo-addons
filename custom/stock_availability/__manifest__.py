{
    'name': 'Stock availability',
    'description': 'stock availability on website',
    'version': '15.0.1.0.0',
    'application': True,
    'depends': [
        'base',
        'website',
        'website_sale',
        'website_slides',
    ],

    'data': [
        'view/stock_availability.xml'
    ],

    'assets': {

        'web.assets_frontend': [
            'stock_availability/static/src/js/stock_availability.js',
        ],

    },
}
