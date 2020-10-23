import json
import logging
import requests
import sys

from .base_handler import BaseHandler
from ..container.docker_service import DockerService

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



class DockerImagesHandler(BaseHandler):

    def post(self, path):
        body = self.get_json_body()
        images = body.get('images')
        ds = DockerService()
        resp = ds.push(images)

        self.finish(json.dumps(resp))


