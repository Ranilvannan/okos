from odoo import models, fields, api


class BlogTemplate(models.Model):
    _name = "blog.template"
    _description = "Blog Template"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    template = fields.Text(string="Template")

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("blog.template")
        return super(BlogTemplate, self).create(vals)
