# -*- coding: utf-8 -*-
{
    'name': "IOT_STOJKO_Ramp",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Data Science",
    'website': "Stojko",
 
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','website_mail'],

    # always loaded
    'data': [
        'security/web_app_security.xml',
        'security/ir.model.access.csv',
        'views/web_app_views.xml',
        'views/config_ramp.xml',
        'views/config_service.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "installable": True,
    "auto_install": False,
}
