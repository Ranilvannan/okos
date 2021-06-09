from odoo import models, fields
from odoo.tools import config
import os
import base64


class Gallery(models.Model):
    _name = "blog.gallery"
    _description = "Blog Galleries"

    file_name = fields.Char(string="Filename")
    file_path = fields.Char(string="Filepath")
    image = fields.Binary(string="Image")

    def trigger_gallery(self):
        root_path = config["technical_blog_root"]
        file_path = os.path.join(root_path, self.file_path)
        image_path = os.path.join(file_path, self.file_name)

        os.makedirs(file_path)
        data = base64.b64decode(self.image)
        with open(image_path, "wb") as imgFile:
            imgFile.write(data)

        self.image = False
