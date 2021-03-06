from odoo import models, fields, api
from datetime import datetime


class Blog(models.Model):
    _name = "blog.blog"
    _description = "Blog"

    date = fields.Date(string="Date", default=datetime.now())
    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
    preview = fields.Text(string="Preview")
    content = fields.Text(string="Content")
    gallery_id = fields.Many2one(comodel_name="blog.gallery", string="Gallery")
    gallery_ids = fields.Many2many(comodel_name="blog.gallery", string="Galleries")
    author_id = fields.Many2one(comodel_name="blog.author", string="Author")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    comments_count = fields.Integer(string="Comment Count", default=0)
    views_count = fields.Integer(string="Views Count", default=0)
    is_completed = fields.Boolean(string="Is Completed")
    date_of_publish = fields.Datetime(string="Date of Publish")
    is_exported = fields.Boolean(string="Is Exported")
    ref = fields.Char(string="Reference")

    _sql_constraints = [
        ('related_blog_uniq', 'unique (ref)', "Reference is not unique !.."),
    ]

    def trigger_duplicate(self):
        self.env["blog.blog"].create({
            "date": self.date,
            "name": self.name,
            "url": self.url,
            "preview": self.preview,
            "content": self.content,
            "gallery_id": self.gallery_id.id,
            "author_id": self.author_id.id,
            "category_id": self.category_id.id,
            "comments_count": self.comments_count,
            "views_count": self.views_count,
            "is_completed": self.is_completed,
        })

    def trigger_blog_export(self):
        self.env["blog.export"].trigger_blog_export()

    def trigger_gallery_export(self):
        self.env["blog.export"].trigger_gallery_export()

    def reset_blog(self):
        self.env["blog.export"].reset_blog()

    def reset_gallery(self):
        self.env["blog.export"].reset_gallery()

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("blog.blog")
        return super(Blog, self).create(vals)
