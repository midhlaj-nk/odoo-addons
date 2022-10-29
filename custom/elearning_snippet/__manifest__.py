{
    'name': 'eLearning Snippet',
    'version': '15.0.1.0.0',
    'depends': ['website', 'base', 'elearning'],
    'summary': 'Dynamic snippet which shows elearning courses.',
    'author': "Midhlaj Nechikkandan",
    'license': 'LGPL-3',

    'application': True,

    'depends': ['base', 'website'],
    'data': ['views/snippet.xml',
             'views/template.xml', ],
    'assets': {

        'web.assets_frontend': [
            'elearning_snippet/static/src/js/snippet.js',
        ],

    },

}
