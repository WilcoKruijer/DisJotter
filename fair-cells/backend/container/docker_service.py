"""
POC: Create a Docker container from a Python script.
"""
import sys
import os
import random
import string

import docker

import traceback

import logging
logger = logging.getLogger('ContainerCreator')
logger.setLevel(logging.DEBUG)


#  Small hack so we can use a dockerfile string instead of having to write it
#  to disk first. See:
#  https://github.com/docker/docker-py/issues/2105#issuecomment-613685891
docker.api.build.process_dockerfile = \
    lambda dockerfile, _: ('Dockerfile', dockerfile)


class DockerService:
    def __init__(self,):
        # self.folder = folder
        # self.name = image_name
        # self.base_image = base_image
        self.client = docker.from_env()

    def get_dockerfile(self,base_image) -> str:
        return (
            "\n".join([
                f'FROM {base_image}',
                f'USER root',
                f'WORKDIR /src/',

                f'COPY ./fair-cells/ /src/fair-cells/',
                f"RUN pip install -r /src/fair-cells/helper/helper_requirements.txt",

                f'COPY ./environment.yml /src/environment.yml',
                f"RUN conda env update --file environment.yml --name base",

                f"USER $NB_UID",

                f'COPY ./notebook.ipynb /src/notebook.ipynb',
                f'COPY ./nb_helper_config.json /src/nb_helper_config.json',

                f'ENTRYPOINT ["python", "-m", "fair-cells"]'
            ])
        )

    def build_container(self, dockerfile: str, folder, image_name) -> docker.api.image.ImageApiMixin:
        #  Save working directory so we can reset it later
        wd = os.getcwd()
        os.chdir(folder)
        logging.info("getcwd: " + str(wd))
        try:
            logging.info("dockerfile: "+str(dockerfile))
            logging.info("Start building container. self.client.images.build")

            image, log = self.client.images.build(tag='fair-cells/'+image_name,
                                            path='.',
                                            dockerfile=dockerfile,
                                            rm=True,
                                            nocache=True)
        except Exception as e:
            logging.error(traceback.format_exc())
        finally:
            #  Change back
            os.chdir(wd)
        logging.info("Returning image and log: "+str(log))
        return image, log

  
    def run_container(self, port=10000,name=None) -> docker.api.container.ContainerApiMixin:
        try:
            cont = self.client.containers.get(name)
            cont.stop(timeout=1)
        except docker.errors.NotFound:
            pass
        logging.info("containers.run name: "+self.name+" ports: "+str(port))
        return self.client.containers.run(self.name,
                    name=name,
                    ports={'8888': port},
                    remove=True,
                    detach=True)
                    # command=f"{port} {code}")

    def login(self,url,username,token):
        logging.info('username: '+username +'password: '+token + 'registry:'+url)
        resp = self.client.login(username=username, password=token, registry=url)
        logging.info("resp: " + str(resp))
        return resp

    def get_local_images(self,tag=None):
        images = []
        for image in self.client.images.list():
            if image.tags:
                if tag:
                    for im_tag in image.tags:
                        if tag in im_tag:
                            ret_image = {'name': im_tag}
                            # ret_image['short_id'] = image.short_id
                            images.append(ret_image)
                elif not tag:
                    ret_image = {'name': image.tags[0]}
                    # ret_image['short_id'] = image.short_id
                    images.append(ret_image)
        return images

    def push(self,images):
        client = docker.from_env()
        logging.info("images: " + str(images))
        results = []
        for image in images:
            logging.info("Pushing: " + str(image.split(':')[0]))
            re = client.images.push(image.split(':')[0])
            logging.info("re: " + str(re))
            results.append(re)
        results
