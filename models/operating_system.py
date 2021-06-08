from odoo import models, fields

CATEGORY = [("windows", "Windows"),
            ("linux", "Linux"),
            ("unix", "Unix"),
            ("android", "Android"),
            ("macos", "Mac OS"),
            ("ios", "IOS")]


class OperatingSystem(models.Model):
    _name = "operating.system"
    _description = "Operating System"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    common_use = fields.Char(string="Common Use")
    ram_usage = fields.Char(string="RAM Usage")
    disk_usage = fields.Char(string="Disk Usage")
    latest_version = fields.Char(string="Latest Version")
    website = fields.Char(string="Website")
    category = fields.Selection(selection=CATEGORY, string="Category")
