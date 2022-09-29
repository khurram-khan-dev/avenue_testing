# -*- coding: utf-8 -*-
{
    'name': "Custom avenue invoices",

    'summary': """
        Custom Invoice requirements for avenue""",

    'description': """
        Custom Invoice requirements for avenue
    """,

    'author': "Khurram",

    
    'category': 'Custom Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'reports/report_button.xml',
        'reports/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
