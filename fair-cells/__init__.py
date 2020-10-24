def _jupyter_server_extension_paths():
    return [{
        "name": "FAIR-Cells",
        "module": "fair-cells",
        "module_name": "fair-cells"
    }]


def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="frontend",
        dest="fair-cells",
        require="fair-cells/index")]


def load_jupyter_server_extension(nbapp):
    from notebook.utils import url_path_join

    from .backend.handlers.environment_handler import EnvironmentHandler
    from .backend.handlers.template_handler import TemplateHandler
    from .backend.handlers.build_handler import BuildHandler
    from .backend.handlers.build_docker_file_handler import BuildDockerFileHandler
    from .backend.handlers.docker_push_handler import DockerPushHandler
    from .backend.handlers.docker_images_handler import DockerImagesHandler
    from .backend.handlers.login_docker_repository_handler import LoginDockerRepositoryHandler
    from .backend.handlers.command_handler import CommandHandler
    from .backend.handlers.inspect_handler import InspectHandler

    nbapp.log.info("FAIR-Cells loaded.")

    web_app = nbapp.web_app
    base = web_app.settings['base_url']

    host_pattern = '.*$'
    build_pattern = url_path_join(base, '/dj/notebook/(.*)/build')
    build_docker_file_pattern = url_path_join(base, '/dj/notebook/(.*)/build_docker_file')
    images_pattern = url_path_join(base, '/dj/notebook/(.*)/images')
    login_docker_repository_pattern = url_path_join(base, '/dj/notebook/(.*)/login')
    push_docker_image_pattern = url_path_join(base, '/dj/notebook/(.*)/push')
    image_command_pattern = url_path_join(base, '/dj/image/(.*)/command/(.*)')
    environment_pattern = url_path_join(base, '/dj/notebook/(.*)/environment')
    inspect_pattern = url_path_join(base, '/dj/notebook/(.*)/inspect/(.*)')

    template_pattern = url_path_join(base, r'/dj/templates/(.*\.(?:html|js|css))')

    web_app.add_handlers(host_pattern, [
        (build_pattern, BuildHandler),
        (build_docker_file_pattern, BuildDockerFileHandler),
        (images_pattern, DockerImagesHandler),
        (login_docker_repository_pattern, LoginDockerRepositoryHandler),
        (push_docker_image_pattern, DockerPushHandler),
        (image_command_pattern, CommandHandler),
        (environment_pattern, EnvironmentHandler),
        (inspect_pattern, InspectHandler),
        (template_pattern, TemplateHandler)])


