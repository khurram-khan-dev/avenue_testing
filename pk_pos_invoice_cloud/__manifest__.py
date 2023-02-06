# -*- coding: utf-8 -*-

{
    'name' : 'POS Integration Cloud',
    'version' : '14.0.6',
    'summary': 'POS Invoice Integration Cloud',
    'description': """POS Invoice Integration Cloud""",
    'depends' : ['point_of_sale', 'product_harmonized_system', 'sh_pos_receipt', 'pos_order_return'],
    'data': [
        #'data/pos_data.xml',
        'security/ir.model.access.csv',
        'security/pos_security.xml',
        'views/assets.xml',
        'views/pos_config.xml',
        'views/res_partner.xml',
        'wizard/fbr_wizard.xml',
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    'installable': True,
    'application': True,
}   
