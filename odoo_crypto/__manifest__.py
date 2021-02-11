# -*- coding: utf-8 -*-
{
    'name': "Crypto Info",
    'summary': """
        Crypto info diary
    """,
    'description': """
        Crypto info diary
    """,
    "category": "Generic Modules",
    "website": "",
    "author": "Raul",
    "license": "LGPL-3",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/crypto_views.xml',
        'views/res_users_views.xml',
        'views/menu_item.xml',
        'data/cron.xml',
        'data/settings.xml'

    ],
    'demo': [],
    "qweb": [],
    'application': True,
    "installable": True,
}
