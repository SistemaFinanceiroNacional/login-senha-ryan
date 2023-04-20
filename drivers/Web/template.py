import os.path
from jinja2 import FileSystemLoader, Environment


templates_path = os.path.dirname(__file__) + "/templates/"
jinja_env = Environment(loader=FileSystemLoader(templates_path))


def render_template(template_name, context):
    template = jinja_env.get_template(template_name)
    return template.render(context)
