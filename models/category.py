from odoo import models, fields
from datetime import datetime


class Category(models.Model):
    _name = "blog.category"
    _description = "Category"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    url = fields.Char(string="URL", required=True)
