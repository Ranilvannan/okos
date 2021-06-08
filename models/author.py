from odoo import models, fields


class Author(models.Model):
    _name = "blog.author"
    _description = "Author Info"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    about_me = fields.Text(string="About Me", required=True)
    photo = fields.Binary(string="Photo")
