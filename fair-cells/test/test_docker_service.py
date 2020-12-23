from unittest import TestCase
from backend.container.docker_service import DockerService

class TestDockerService(TestCase):

    def test_get_dockerfile(self):
        pass

    def test_build_container(self):
        pass

    def test_run_container(self):
        pass

    def test_login(self):
        pass


    def test_get_local_images(self):
        pass

    def test_push(self):
        cc = DockerService()
        out = cc.login(url='https://index.docker.io/v1/',username='alogo53',token='9bf63a99-554d-40ec-8088-de26a3cb3351')
        self.assertIsNotNone(out)
        images = cc.get_local_images('cloudcells/classifiers')
        out = cc.push(images)
        print(out)


    def test_get_image_status(self):
        self.fail()

    def test_stop_image(self):
        pass

    def test_get_container(self):
        pass
