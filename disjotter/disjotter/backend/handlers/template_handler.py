from tornado.web import RequestHandler, HTTPError
from tornado import template

import os

class TemplateHandler(RequestHandler):
    def get(self, path):
        args = None

        if path == 'form.html':
            base_images = [
                ('Base Notebook', 'jupyter/base-notebook'),
                ('Minimal Notebook', 'jupyter/minimal-notebook'),
                ('R Notebook', 'jupyter/r-notebook'),
                ('Scipy Notebook', 'jupyter/scipy-notebook'),
                ('Data Science Notebook', 'jupyter/datascience-notebook')
            ]

            base_images.reverse()

            args = {
                'images': base_images
            }

        try:
            if args is None:
                args = {}

            self.render(path, **args)
        except FileNotFoundError as e:
            raise HTTPError(404)

    def get_template_path(self):
        dirname = os.path.dirname(__file__)

        return os.path.join(dirname + "/../templates")