import os.path

from drivers.Web.lexer import lexer, auxiliar_lexer
import drivers.Web.parser as parser

templates_path = os.path.dirname(__file__) + "/templates/"

def render_template(template_name, context, file_lexer=None):
    lexer_of_file = file_lexer or file_system_file_lexer
    alexer = lexer_of_file(template_name)
    return parser.parser(alexer, lexer_of_file).render(context, {})


def file_system_file_lexer(template_name):
    file_name = templates_path + template_name
    with open(file_name) as file:
        file_content = file.read()

    lxer = lexer(file_content)
    return auxiliar_lexer(lxer)

