# -*- coding: utf-8 -*-
{
    'name': "Steven Test",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TresCloud",
    'website': "https://www.trescloud.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale_management',
        'stock',
        'hr'
        ],

    # always loaded
    'data': [
        # Data
        'data/enrollment_sequence.xml',
        
        # Views
        'views/subject_view.xml',
        'views/res_partner_view.xml',
        'views/enrollment_view.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/career_enrollment_view.xml',
        'views/student_subject_view.xml',
        
        # Security
        'security/ir.model.access.csv',
        
        # Reports
        'reports/enrollment.xml',
        'views/templates.xml',
        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
