from odoo import models, fields


class BlogRelated(models.Model):
    _name = "blog.related"
    _description = "Blog Related"

    blog_id = fields.Many2one(comodel_name="blog.blog", string="Blog")
    related_ids = fields.Many2many(comodel_name="blog.blog", string="Related")

    _sql_constraints = [
        ('related_blog_uniq', 'unique (blog_id)', "Blogs related is not unique !.."),
    ]
