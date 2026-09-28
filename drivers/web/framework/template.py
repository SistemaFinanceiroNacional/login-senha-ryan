import os.path
from functools import cache
from jinja2 import FileSystemLoader, Environment, select_autoescape
import logging
from drivers.web.framework import settings


logger = logging.getLogger("drivers.web.framework.template")


@cache
def get_jinja_env():
    # Imported here: the CSRF module builds responses, which render
    # templates.
    from drivers.web.framework.httprequest.csrf import csrf_token

    abs_path_project = settings.app_settings.BASE_DIR
    template_path = settings.app_settings.TEMPLATES
    templates_path = os.path.join(abs_path_project, template_path)
    # Every value interpolated into an HTML template is escaped, so user
    # data is always text, never markup.
    environment = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
    )
    environment.globals["csrf_token"] = csrf_token
    return environment


def render_template(template_name, context):
    jinja_env = get_jinja_env()
    template = jinja_env.get_template(template_name)
    return template.render(context)
