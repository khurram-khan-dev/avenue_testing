# -*- coding: utf-8 -*-


{
    'name': 'Sales Qoutation Extension',

    "author": "khurram,Pooran",
    'version': '0.1',
    'category': 'Sale',
    'sequence': 95,
    'summary': 'Custom Requirements of Avennue Sales Qoutation.',
    'description': "Custom Requirements of Avennue Sales Qoutation.",
    'website': '',
    'images': [
    ],
    'depends': ['base','sale','account'],
    'data': [
        "views/sq_ext.xml",
        "views/sq_tree.xml",
    ],
    'demo': [
        
        # "views/sale_analysis_report.xml",
        # "views/inherit_sale_report.xml",
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
    ],
    'license': 'LGPL-3',
}
