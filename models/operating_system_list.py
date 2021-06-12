from odoo import models, fields
from jinja2 import Template


class OperatingSystemList(models.Model):
    _name = "ops.list"
    _description = "Operating System List"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    template_id = fields.Many2one(comodel_name="blog.template")
    item_ids = fields.Many2many(comodel_name="operating.system", string="Items")

    def trigger_generate_blog(self):
        html = Template(self.template_id.template)
        return html.render(items=self.item_ids)

