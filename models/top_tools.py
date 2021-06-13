from odoo import models, fields, api
from jinja2 import Template


class TopTools(models.Model):
    _name = "top.tools"
    _description = "Top Tools"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name")
    content = fields.Text(string="Content")
    tools_ids = fields.Many2many(comodel_name="blog.tools")
    template_id = fields.Many2one(comodel_name="blog.template")

    def trigger_generate_blog(self):
        html = Template(self.template_id.template)
        list_data = html.render(items=self.tools_ids)

        content = "{0}\n{1}".format(self.content, list_data)

        rec = self.env["blog.blog"].search([("ref", "=", self.sequence)])
        if not rec:
            self.env["blog.blog"].create({"name": self.name, "content": content})

        if rec:
            rec.name = self.name
            rec.content = self.content

        return True

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("top.tools")
        return super(TopTools, self).create(vals)
