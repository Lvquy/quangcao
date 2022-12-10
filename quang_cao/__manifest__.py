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
    'depends': ['base_setup', 'website_sale','website','website_blog'],
    'data': [
        #data
        'data/cronjob.xml',
        'data/email_template.xml',
        'data/sequence.xml',
        # security
        'security/groups.xml',
        'security/ir.model.access.csv',
        # report
        'report/cham_cong.xml',
        'report/tong_cong.xml',
        'report/menu_print.xml',

        # views
        'views/hide_add_to_cart_btn.xml',
        'views/custom_page.xml',
        'views/custom_footer.xml',
        'views/seo_web.xml',
        'views/res_config_setting.xml',
        'views/key_log_ranking.xml',
        'views/blog_content_backend.xml',
        'views/sale.xml',
        'views/purchase.xml',
        'views/pay_lines.xml',
        'views/res_company.xml',
        'views/cham_cong.xml',
        'views/tong_cong.xml',
        'views/ung_luong.xml',
        'views/hr_employee.xml',
        'views/search.xml',
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
