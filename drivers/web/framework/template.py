import inspect
import os.path
from types import ModuleType
from jinja2 import FileSystemLoader, Environment
import logging


logger = logging.getLogger("drivers.web.framework.template")
jinja_env = Environment(loader=FileSystemLoader(""))


def render_template(template_name, context):
    template = jinja_env.get_template(template_name)
    return template.render(context)


def configure_template(module: ModuleType):
    global jinja_env
    abs_path_project = os.path.dirname(inspect.getfile(module))
    logger.debug(f"Absolute path of project: {abs_path_project}")
    template_path = module.TEMPLATES
    logger.debug(f"Template path: {template_path}")
    templates_path = os.path.join(abs_path_project, template_path)
    logger.debug(f"Templates path joint: {templates_path}")
    jinja_env = Environment(loader=FileSystemLoader(templates_path))
