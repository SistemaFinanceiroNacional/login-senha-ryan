import os.path
from functools import cache
from jinja2 import FileSystemLoader, Environment
import logging
from drivers.web.framework import settings


logger = logging.getLogger("drivers.web.framework.template")

@cache
def get_jinja_env():
    abs_path_project = settings.app_settings.BASE_DIR
    template_path = settings.app_settings.TEMPLATES
    templates_path = os.path.join(abs_path_project, template_path)
    return Environment(loader=FileSystemLoader(templates_path))


def render_template(template_name, context):
    jinja_env = get_jinja_env()
    template = jinja_env.get_template(template_name)
    return template.render(context)
