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
        'security/ir.model.access.csv',
        # views
        'views/hide_add_to_cart_btn.xml',
        'views/custom_page.xml',
        'views/custom_footer.xml',
        'views/seo_web.xml',
        'views/res_config_setting.xml',
        'views/key_log_ranking.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'quang_cao/static/src/css/style.css'
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
}
