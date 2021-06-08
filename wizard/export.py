from odoo import models, fields, api, exceptions
from odoo.tools import config
import os
import json
from datetime import datetime
import tempfile
from paramiko import SSHClient, AutoAddPolicy


class Export(models.TransientModel):
    _name = "blog.export"
    _description = "Blog Export"

    def trigger_technical_blog_export(self):
        variety = config["technical_blog_export_variety"]

        recs = self.env["blog.blog"].search([("variety_id.name", "=", variety),
                                             ("is_completed", "=", True),
                                             ("is_exported", "=", False)])[:10]

        if recs:
            data = self.generate_json(recs)

            # Articles Export
            tmp_file = self.generate_tmp_json_file(data["articles"])
            # self.move_tmp_file(tmp_file)

        for rec in recs:
            rec.is_exported = True

    def generate_json(self, recs):
        articles = []

        for rec in recs:
            blog = {
                "date": "Date",
                "sequence": rec.sequence,
                "name": rec.name,
                "url": rec.url,
                "image": rec.image,
                "preview": rec.preview,
                "content": rec.content,
                "author_name": rec.author_id.name,
                "author_email": rec.author_id.email,
                "author_description": rec.author_id.about_me
            }

            articles.append(blog)

        return {"articles": articles}

    def generate_tmp_json_file(self, json_data):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".json", delete=False, mode="w+")
        json.dump(json_data, tmp_file)
        tmp_file.flush()
        print(tmp_file)

        return tmp_file

    def move_tmp_file(self, tmp_file):
        host = config["technical_blog_export_host"]
        username = config["technical_blog_export_username"]
        key_filename = config["technical_blog_export_public_key_filename"]
        path = config["technical_blog_path"]

        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, key_filename=key_filename)
        sftp_client = ssh_client.open_sftp()
        filename = os.path.basename(tmp_file.name)
        local_path = tmp_file.name
        remote_path = os.path.join(path, filename)
        sftp_client.put(local_path, remote_path)
        sftp_client.close()
        tmp_file.close()

        return True
