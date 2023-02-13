import drivers.Web.lexer as lexer
import drivers.Web.parser as parser

def test_parser_using_empty_lexer():
    lxer = lexer.lexer("")
    prser = parser.parser(lxer)
    parser_str = prser.render({})
    assert parser_str == ""

def test_parser_using_empty_lexer_no_empty_context():
    lxer = lexer.lexer("")
    prser = parser.parser(lxer)
    parser_str = prser.render({"is_authenticated": False})
    assert parser_str == ""

def test_parser_lexer_with_string():
    lxer = lexer.lexer("lorem ipsum")
    prser = parser.parser(lxer)
    parser_str = prser.render({})
    assert parser_str == "lorem ipsum"

def test_parser_lexer_with_variable1():
    lxer = lexer.lexer("{{ is_authenticated }}")
    prser = parser.parser(lxer)
    parser_str = prser.render({"is_authenticated": True})
    assert parser_str == "True"