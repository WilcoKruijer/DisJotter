def _jupyter_server_extension_paths():
    return [{
        "name": "DisJotter",
        "module": "disjotter",
        "module_name": "disjotter"
    }]


def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="frontend",
        dest="disjotter",
        require="disjotter/index")]


def load_jupyter_server_extension(nbapp):
    from notebook.utils import url_path_join

    from .backend.handlers.environment_handler import EnvironmentHandler
    from .backend.handlers.template_handler import TemplateHandler
    from .backend.handlers.build_handler import BuildHandler
    from .backend.handlers.command_handler import CommandHandler
    from .backend.handlers.inspect_handler import InspectHandler

    nbapp.log.info("DisJotter loaded.")

    web_app = nbapp.web_app
    base = web_app.settings['base_url']

    host_pattern = '.*$'
    build_pattern = url_path_join(base, '/dj/notebook/(.*)/build')
    image_command_pattern = url_path_join(base, '/dj/image/(.*)/command/(.*)')
    environment_pattern = url_path_join(base, '/dj/notebook/(.*)/environment')
    inspect_pattern = url_path_join(base, '/dj/notebook/(.*)/inspect/(.*)')

    template_pattern = url_path_join(base, r'/dj/templates/(.*\.(?:html|js|css))')

    web_app.add_handlers(host_pattern, [
        (build_pattern, BuildHandler),
        (image_command_pattern, CommandHandler),
        (environment_pattern, EnvironmentHandler),
        (inspect_pattern, InspectHandler),
        (template_pattern, TemplateHandler)])


