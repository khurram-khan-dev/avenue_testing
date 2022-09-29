# -*- coding: utf-8 -*-


{
    'name': 'Sales Invoice Avennue Extension',

    "author": "Khurram Khan",
    'version': '0.1',
    'category': 'Sale',
    'sequence': 95,
    'summary': 'Custom Requirements of Avennue for invoice.',
    'description': "Custom Requirements of Avennue for invoice.",
    'website': '',
    'images': [
    ],
    'depends': ['base','account','sale','sq_ext'],
    'data': [
        'views/inv_ext.xml',
        # 'reports/report_button.xml',
        # 'reports/invoice_report.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
    ],
    'license': 'LGPL-3',
}
