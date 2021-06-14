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

    def reset_blog(self):
        variety = config["technical_blog_export_variety"]
        recs = self.env["blog.blog"].search([("variety_id.name", "=", variety)])

        for rec in recs:
            rec.is_exported = False

    def trigger_technical_blog_export(self):
        variety = config["technical_blog_export_variety"]

        recs = self.env["blog.blog"].search([("variety_id.code", "=", variety),
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
            previous_blog_name = False
            previous_blog_url = False
            previous_articles = self.env["blog.blog"].search([("id", "<", rec.id)])
            if previous_articles:
                previous_blog = previous_articles[-1]
                previous_blog_name = previous_blog.name
                previous_blog_url = previous_blog.url

            next_blog_name = False
            next_blog_url = False
            next_articles = self.env["blog.blog"].search([("id", ">", rec.id)])
            if next_articles:
                next_blog = next_articles[0]
                next_blog_name = next_blog.name
                next_blog_url = next_blog.url

            related_articles = self.env["blog.related"].search([("blog_id", "=", rec.id)])

            blog = {
                "blog_id": rec.id,
                "date_us_format": rec.date.strftime("%Y-%m-%d"),
                "date_read_format": rec.date.strftime("%d %b %Y"),
                "date_lastmod": rec.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "sequence": rec.sequence,
                "name": rec.name,
                "url": rec.url,
                "image_file": rec.gallery_id.file_name,
                "image_file_path": rec.gallery_id.file_path,
                "items": [{"image_file": item.gallery_id.file_name,
                           "image_file_path": item.gallery_id.file_path} for item in rec.item_ids],
                "preview": rec.preview,
                "content": rec.content,
                "author_name": rec.author_id.name,
                "author_email": rec.author_id.email,
                "author_description": rec.author_id.about_me,
                "author_photo_image_file": rec.author_id.gallery_id.file_name,
                "author_photo_image_file_path": rec.author_id.gallery_id.file_path,
                "category_name": rec.category_id.name,
                "category_url": rec.category_id.url,
                "variety": rec.variety_id.name,
                "blog_code": rec.variety_id.code,
                "comments_count": 0,
                "views_count": 0,
                "previous_blog_name": previous_blog_name,
                "previous_blog_url": previous_blog_url,
                "next_blog_name": next_blog_name,
                "next_blog_url": next_blog_url,
                "related_blogs": [{"image_file": item.gallery_id.file_name,
                                   "image_file_path": item.gallery_id.file_path,
                                   "name": item.name,
                                   "url": item.url} for item in related_articles.related_ids]
            }

            articles.append(blog)

        return {"articles": articles}

    def generate_tmp_json_file(self, json_data):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".json", delete=False, mode="w+")
        json.dump(json_data, tmp_file)
        tmp_file.flush()

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
