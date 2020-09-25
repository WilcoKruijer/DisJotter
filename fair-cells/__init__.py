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
    from .backend.handlers.build_handler import BuildContainerHandler
    from .backend.handlers.command_handler import CommandHandler
    from .backend.handlers.inspect_handler import InspectHandler

    nbapp.log.info("FAIR-Cells loaded.")

    web_app = nbapp.web_app
    base = web_app.settings['base_url']

    host_pattern = '.*$'
    build_pattern = url_path_join(base, '/fair-cells/notebook/(.*)/build')
    image_command_pattern = url_path_join(base, '/fair-cells/image/(.*)/command/(.*)')
    environment_pattern = url_path_join(base, '/fair-cells/notebook/(.*)/environment')
    inspect_pattern = url_path_join(base, '/fair-cells/notebook/(.*)/inspect/(.*)')

    template_pattern = url_path_join(base, r'/fair-cells/templates/(.*\.(?:html|js|css))')

    web_app.add_handlers(host_pattern, [
        (build_pattern, BuildContainerHandler),
        (image_command_pattern, CommandHandler),
        (environment_pattern, EnvironmentHandler),
        (inspect_pattern, InspectHandler),
        (template_pattern, TemplateHandler)])


