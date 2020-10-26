import json
import logging

from .base_handler import BaseHandler
from ..container.docker_service import DockerService

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



class DockerPublishHandler(BaseHandler):

    def post(self, path):
        body = self.get_json_body()
        images = body.get('images')
        logging.info("images: " + str(images))
        ds = DockerService()
        resp = ds.push(images)

        self.finish(json.dumps(resp))


