# -*- coding: utf-8 -*-
{
    'name': 'Quảng cáo Trường Phát',
    'version': '1',
    'category': 'Quảng cáo Trường Phát',
    'live_test_url': '#',
    'summary': 'Phần mềm quản lý - Trường Phát',
    'author': 'Lv Quy',
    'company': 'Trường Phát',
    'website': 'https://#',
    'depends': ['base_setup', 'prt_report_attachment_preview', 'rowno_in_tree', 'web_responsive','website'],
    'data': [
        # security
        # 'security/groups.xml',
        # 'security/ir.model.access.csv',
        # views
        'views/hide_add_to_cart_btn.xml',
        'views/team.xml',
        'views/custom_footer.xml',
        #template
        # menu
        # report

    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
}
