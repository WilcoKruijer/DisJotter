import json
import logging
import requests
import sys

from .base_handler import BaseHandler
from ..container.docker_service import DockerService

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



class LoginDockerRepositoryHandler(BaseHandler):

    def post(self, path):
        body = self.get_json_body()

        docker_repository = body.get('docvariableskerRepository')
        docker_username = body.get('dockerUsername')
        docker_token = body.get('dockerToken')
        variables = body.get('variables', {})
        logging.info("docker_repository: " + str(docker_repository))
        logging.info("docker_username: " + str(docker_username))
        logging.info("docker_token: " + str(docker_token))

        ds = DockerService()
        # try:
        resp = ds.login(username=docker_username,token=docker_username,url=docker_repository)
        logging.info("resp: " + resp)
        self.finish(json.dumps({
            'dockerLogin': resp
        }))
        # except requests.exceptions.HTTPError as e:
        #     logging.warning("e: " + str(e))
        #     error = self.write_error(e.status_code, exc_info=sys.exc_info())
        #     logging.warning("error: " + str(error))

