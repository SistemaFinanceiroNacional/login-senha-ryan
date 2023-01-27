import os.path

templates_path = os.path.dirname(__file__) + "/templates/"

def render_template(template_name, context):
    file_name = templates_path + template_name
    with open(file_name) as file:
        file_content = file.read()

    for key, value in context.items():
        file_content = file_content.replace(f"{{{key}}}", value)

    return file_content
