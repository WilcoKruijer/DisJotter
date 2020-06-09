"""
POC: Create a Docker container from a Python script.
"""
import sys
import os
import random
import string

import docker


#  Small hack so we can use a dockerfile string instead of having to write it
#  to disk first. See:
#  https://github.com/docker/docker-py/issues/2105#issuecomment-613685891
docker.api.build.process_dockerfile = \
    lambda dockerfile, _: ('Dockerfile', dockerfile)


class ContainerCreator:
    def __init__(self, folder, image_name, base_image):
        self.folder = folder
        self.name = image_name
        self.base_image = base_image
        self.client = docker.from_env()

    def get_dockerfile(self) -> str:
        return (
            #  TODO : Optimize this Dockerfile to properly use cache.
            "\n".join([
                f'FROM {self.base_image}',
                f'WORKDIR /src/',
                f'COPY . /src/',
                f"RUN pip install -r /src/helper/helper_requirements.txt && \\",
                f"pip install -r /src/requirements.txt",
                f'ENTRYPOINT ["python", "helper/helper_main.py"]'
            ])
        )

    def build_container(self, dockerfile: str) -> docker.api.image.ImageApiMixin:
        # os.system(f"docker build -f /tmp/Dockerfile -t {self.name} .")

        #  Save working directory so we can reset it later
        wd = os.getcwd()
        print('saving wd', wd)
        os.chdir(self.folder)

        image, log = self.client.images.build(tag=self.name, 
                                        path='.',
                                        dockerfile=dockerfile,
                                        rm=True)

        #  Change back
        os.chdir(wd)

        return image, log

  
    def run_container(self, port=10000) -> docker.api.container.ContainerApiMixin:
    # status = os.system(f"docker run --rm -d -p 8111:8111 --name {self.name} {self.name}")
        try:
            cont = self.client.containers.get(self.name)
            cont.stop(timeout=1)
        except docker.errors.NotFound:
            pass
    
        return self.client.containers.run(self.name,
                    name=self.name,
                    ports={'8888': port},
                    remove=True,
                    detach=True)
                    # command=f"{port} {code}")

