from odoo import models, fields, api
from datetime import datetime


class Blog(models.Model):
    _name = "blog.blog"
    _description = "Blog"

    date = fields.Date(string="Date", default=datetime.now())
    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name", required=True)
    url = fields.Char(string="URL", required=True)
    preview = fields.Text(string="Preview")
    content = fields.Text(string="Content")
    gallery_id = fields.Many2one(comodel_name="blog.gallery", string="Gallery")
    item_ids = fields.One2many(comodel_name="blog.items", inverse_name="blog_id")
    author_id = fields.Many2one(comodel_name="blog.author", string="Author")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    variety_id = fields.Many2one(comodel_name="blog.variety", string="Variety")
    comments_count = fields.Integer(string="Comment Count", default=0)
    views_count = fields.Integer(string="Views Count", default=0)
    is_completed = fields.Boolean(string="Is Completed")
    date_of_publish = fields.Datetime(string="Date of Publish")
    is_exported = fields.Boolean(string="Is Exported")

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("blog.blog")
        return super(Blog, self).create(vals)


class BlogItems(models.Model):
    _name = "blog.items"
    _description = "Blog Items"

    gallery_id = fields.Many2one(comodel_name="blog.gallery", string="Gallery")
    blog_id = fields.Many2one(comodel_name="blog.blog", string="Blog")
