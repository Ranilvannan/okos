from odoo import models
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
        recs = self.env["blog.blog"].search([("id", ">", 0)])

        for rec in recs:
            rec.is_exported = False

    def reset_gallery(self):
        recs = self.env["blog.gallery"].search([("id", ">", 0)])

        for rec in recs:
            rec.is_exported = False

    def trigger_blog_export(self):
        blog_filename = config["export_blog_filename"]

        # Articles Export
        recs = self.env["blog.blog"].search([("is_completed", "=", True), ("is_exported", "=", False)])[:10]
        if recs:
            data = self.generate_variety_json(recs)
            tmp_file = self.generate_tmp_json_file(data["articles"], blog_filename)
            # self.move_tmp_file(tmp_file)

        for rec in recs:
            rec.is_exported = True

    def trigger_gallery_export(self):
        gallery_filename = config["export_gallery_filename"]

        # Gallery Export
        recs = self.env["blog.gallery"].search([("is_exported", "=", False)])[:500]
        if recs:
            data = self.generate_gallery_json(recs)
            tmp_file = self.generate_tmp_json_file(data["galleries"], gallery_filename)
            # self.move_tmp_file(tmp_file)

        for rec in recs:
            rec.is_exported = True

    def generate_variety_json(self, recs):
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
                "blog_code": config["export_blog_code"],
                "date_us_format": rec.date.strftime("%Y-%m-%d"),
                "date_read_format": rec.date.strftime("%d %b %Y"),
                "date_lastmod": rec.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "sequence": rec.sequence,
                "name": rec.name,
                "url": rec.url,
                "image_filename": rec.gallery_id.filename,
                "image_filepath": rec.gallery_id.filepath,
                "galleries": [{"image_filename": gallery.filename,
                               "image_filepath": gallery.filepath} for gallery in rec.gallery_ids],
                "preview": rec.preview,
                "content": rec.content,
                "author_name": rec.author_id.name,
                "author_email": rec.author_id.email,
                "author_description": rec.author_id.about_me,
                "author_image_filename": rec.author_id.gallery_id.filename,
                "author_image_filepath": rec.author_id.gallery_id.filepath,
                "category_name": rec.category_id.name,
                "category_url": rec.category_id.url,
                "comments_count": 0,
                "views_count": 0,
                "previous_blog_name": previous_blog_name,
                "previous_blog_url": previous_blog_url,
                "next_blog_name": next_blog_name,
                "next_blog_url": next_blog_url,
                "related_blogs": [{"image_filename": item.gallery_id.filename,
                                   "image_filepath": item.gallery_id.filepath,
                                   "name": item.name,
                                   "url": item.url} for item in related_articles.related_ids]
            }

            articles.append(blog)

        return {"articles": articles}

    def generate_gallery_json(self, recs):
        galleries = []

        for rec in recs:
            image = {
                "gallery_id": rec.id,
                "filename": rec.filename,
                "filepath": rec.filepath,
                "description": rec.description
            }
            galleries.append(image)

        return {"galleries": galleries}

    def generate_tmp_json_file(self, json_data, filename):
        prefix = datetime.now().strftime('%s')
        suffix = "{filename}.json".format(filename=filename)
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        json.dump(json_data, tmp_file)
        tmp_file.flush()

        return tmp_file

    def move_tmp_file(self, tmp_file):
        host = config["export_host"]
        username = config["export_username"]
        key_filename = config["export_public_key"]
        path = config["export_path"]

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
