from odoo import models, fields


class Variety(models.Model):
    _name = "blog.variety"
    _description = "Blog Variety"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
