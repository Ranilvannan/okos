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
    description = fields.Char(string="Description")

    def trigger_gallery(self):
        root_path = config["technical_blog_root"]
        file_path = os.path.join(root_path, self.file_path)
        image_path = os.path.join(file_path, self.file_name)
        is_directory_available = os.path.isdir(file_path)

        if not is_directory_available:
            os.makedirs(file_path)

        data = base64.b64decode(self.image)
        with open(image_path, "wb") as imgFile:
            imgFile.write(data)

        self.image = False
