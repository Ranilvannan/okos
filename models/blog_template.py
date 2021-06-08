from odoo import models, fields


class BlogTemplate(models.Model):
    _name = "blog.template"
    _description = "Blog Template"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
    template = fields.Text(string="Template")
