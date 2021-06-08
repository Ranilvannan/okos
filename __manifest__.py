# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Okos',
    'version': '1.1',
    'summary': 'Okos',
    'sequence': 1,
    'description': 'Okos',
    'category': 'New',
    'website': '',
    'images': [],
    'depends': ['base', 'web', 'mail'],
    'data': [
        'data/sequence.xml',
        'security/okos_security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/author_view.xml',
        'views/category_view.xml',
        'views/variety_view.xml',
        'views/blog_view.xml',
        'views/blog_template_view.xml',
        'views/operating_system_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}