import drivers.Web.lexer as lexer
import drivers.Web.parser as parser

def fake_lexer_function():
    raise NotImplemented()

def test_parser_using_empty_lexer():
    lxer = lexer.lexer("")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({}, {})
    assert parser_str == ""

def test_parser_using_empty_lexer_no_empty_context():
    lxer = lexer.lexer("")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({"is_authenticated": False}, {})
    assert parser_str == ""

def test_parser_lexer_with_string():
    lxer = lexer.lexer("lorem ipsum")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({}, {})
    assert parser_str == "lorem ipsum"

def test_parser_lexer_with_variable1():
    lxer = lexer.lexer("{{ is_authenticated }}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({"is_authenticated": True}, {})
    assert parser_str == "True"

def test_parser_with_str_constant_to_get_username():
    lxer = lexer.lexer("Your username is {{ username }}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({"username": "Ryan"}, {})
    assert parser_str == "Your username is Ryan"

def test_parser_with_str_constant_and_block():
    lxer = lexer.lexer("Your username is {% block title %}lorem ipsum{% endblock %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    prser = parser.parser(aux_lexer, fake_lexer_function)
    parser_str = prser.render({"username": "Ryan"}, {})
    assert parser_str == "Your username is lorem ipsum"

def test_lexer_statements_for_a_block_token():
    lxer = lexer.lexer("{% block title %}lorem ipsum{% endblock %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    block_statement = parser.parser_block(aux_lexer, fake_lexer_function)
    assert block_statement == parser.BLOCK("title", parser.STATEMENTS([parser.STRING_CONSTANT("lorem ipsum")]))

def test_parser_statements_for_a_identifier():
    lxer = lexer.lexer("{{ username }}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    identifier_statement = parser.parser_identifier(aux_lexer)
    assert identifier_statement == parser.IDENTIFIER("username")

def test_parser_statements_for_a_extends():
    lxer = lexer.lexer("{% extends base.html %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    extends_statement = parser.parser_extends(aux_lexer, fake_lexer_function)
    assert extends_statement == parser.EXTENDS("base.html", fake_lexer_function)

def test_parser_base_template_render():
    lxer = lexer.lexer("Before block statement {% block title %}inside base block{% endblock %} after block")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    assert parser.parser(aux_lexer, fake_lexer_function).render({}, {}) == "Before block statement inside base block after block"

def test_parser_base_template_render_changing_block():
    lxer = lexer.lexer("Before block statement {% block title %}inside base block{% endblock %} after block")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    assert parser.parser(aux_lexer, fake_lexer_function).render({}, {"title": parser.BLOCK("title", parser.STATEMENTS([parser.STRING_CONSTANT("inside child block")]))})\
           == "Before block statement inside child block after block"

def test_parser_child_template():
    def lexer_function(name):
        if name == "base.html":
            return lexer.auxiliar_lexer(lexer.lexer("Start of base {% block title %}inside base block{% endblock %} after base block"))
    lxer = lexer.lexer("{% extends base.html %} {% block title %}inside child block{% endblock %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    renderized_parser = parser.parser(aux_lexer, lexer_function).render({}, {})
    assert renderized_parser == "Start of base inside child block after base block"
