from odoo import models, fields, api


class Author(models.Model):
    _name = "blog.author"
    _description = "Author Info"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    about_me = fields.Text(string="About Me", required=True)
    photo = fields.Binary(string="Photo")
    url = fields.Char(string="URL")

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("blog.author")
        return super(Author, self).create(vals)

