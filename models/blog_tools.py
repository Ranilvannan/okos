from odoo import models, fields


class BlogTools(models.Model):
    _name = "blog.tools"
    _description = "Blog Tools"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    content = fields.Text(string="Content")
    feature_ids = fields.One2many(comodel_name="blog.tools.item", inverse_name="tool_id")
    website = fields.Char(string="Website")


class BlogToolsItem(models.Model):
    _name = "blog.tools.item"
    _description = "Blog Tools Item"

    name = fields.Char(string="Name")
    tool_id = fields.Many2one(comodel_name="blog.tools", string="Blog Tool")
