# -*- coding: utf-8 -*-

from odoo import fields, api, models
from datetime import datetime
import requests
import urllib.parse as p



class SEO(models.Model):
    _name = 'seo.web'
    _rec_name = 'name'
    _description = 'Seo website trên google search'

    name = fields.Char(string='Dự án')
    website = fields.Char(string='Website')
    start_date = fields.Date(string='Ngày bắt đầu dự án', default=datetime.today())
    end_date = fields.Date(string='Ngày kết thúc')
    nguoi_tham_gia = fields.Many2many(comodel_name='res.users', string='Người tham gia')
    keywords = fields.One2many(comodel_name='list.keyword', inverse_name='du_an', string='Danh sách từ khóa')
    note = fields.Text(string='Note')
    state = fields.Selection([('0','New'),('1','Đang seo'),('2','Hoàn thành')],string='Trạng thái',default='0')
    target_domain = fields.Char(string='Tên miền kiểm tra')
    page = fields.Integer(string='Trang thứ', default=1)

    def confirm(self):
        self.state = '1'
    def done(self):
        self.state = '2'

    def create_log(self):
        for rec in self:
            LOG = rec.env['log.ranking']
            for i in rec.keywords:
                LOG.create({
                    'date_ranking': datetime.today(),
                    'project_of': rec.id,
                    'keyword_list':[(0, 0, {
                        'name': i.name,
                        'ranking':i.thu_hang,
                    })],
                })

    def update_ranking(self, target_domain, query,page):
        ICP = self.env['ir.config_parameter'].sudo()
        API_KEY = ICP.get_param('quang_cao.API_KEY')
        SEARCH_ENGINE_ID = ICP.get_param('quang_cao.SEARCH_ENGINE_ID')
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
        data = requests.get(url).json()
        search_items = data.get("items")
        for i, search_item in enumerate(search_items, start=1):
            link = search_item.get("link")
            if target_domain in link:
                return i

    def check_ranking(self):
        for rec in self:
            rec.create_log()
            for k in rec.keywords:
                query = k.name
                rank = rec.update_ranking(target_domain=rec.target_domain,query=query, page=rec.page)
                k.old_rank = k.thu_hang
                if rank:
                    k.thu_hang = (10*rec.page + rank) - 10
                    k.date_update = datetime.today()
                    k.target_domain = rec.target_domain





class ListKeyword(models.Model):
    _name = 'list.keyword'
    _rec_name = 'name'
    _description = 'List keyword'

    name = fields.Char(string='Từ khóa')
    search_count_pm = fields.Integer(string='Số lần tìm kiếm TB / Tháng')
    canh_tranh = fields.Selection([('0','Thấp'),('1','Trung bình'),('2','Cao')],string='Cạnh tranh')
    thu_hang = fields.Integer(string='Thứ hạng')
    old_rank = fields.Integer(string='Thứ hạng cũ')
    date_update = fields.Date(string='Ngày cập nhật')
    du_an = fields.Many2one(comodel_name='seo.web', string='Dự án')
    target_domain = fields.Char(string='Tên miền kiểm tra')

    def view_blog(self,):
        import unidecode
        # Xóa dấu unicode để so sánh
        field_ids = self.env['blog.post'].search(['|',('website_meta_keywords','ilike',self.name),('website_meta_keywords', 'ilike', unidecode.unidecode(self.name))]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "blog.post.list")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'blog.post',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Bài viết theo từ khóa: %s' %(self.name)
        }

class LogRanking(models.Model):
    _name = 'log.ranking'
    _rec_name = 'date_ranking'
    _description = 'Log Ranking'

    date_ranking = fields.Date(string='Ngày ghi nhận', default=datetime.today())
    project_of = fields.Many2one(comodel_name='seo.web', string='Dự án')
    keyword_list = fields.One2many(comodel_name='key.list.log', inverse_name='ref_log_ranking', string='Keywords')

class KeywordListLong(models.Model):
    _name = 'key.list.log'
    _rec_name = 'name'
    _description = 'Keyword List Log'

    name = fields.Char(string='Từ khóa')
    ranking = fields.Integer(string='Thứ hạng')
    ref_log_ranking = fields.Many2one(comodel_name='log.ranking', string='Log Keyword ranking')

class BlogPost(models.Model):
    _inherit = 'blog.post'

    def test(self):
        print(self.content)