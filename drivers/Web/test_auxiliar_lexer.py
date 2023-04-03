import drivers.Web.lexer as lexer


def test_auxiliar_lexer():
    lxer = lexer.lexer("Your username is {% block title %}one{% endblock %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    assert aux_lexer.peek() == lexer.STRING_CONSTANT_CLASS("Your username is ")


def test_auxiliar_lexer_doesnot_consume_lexer():
    lxer = lexer.lexer("Your username is {% block title %}one{% endblock %}")
    aux_lexer = lexer.auxiliar_lexer(lxer)
    aux_lexer.peek()
    aux_lexer_as_list = list(aux_lexer)
    assert aux_lexer_as_list == [lexer.STRING_CONSTANT_CLASS("Your username is "),
                                 lexer.BLOCK,
                                 lexer.STRING_CONSTANT_CLASS("title"),
                                 lexer.STRING_CONSTANT_CLASS("one"),
                                 lexer.END_BLOCK]
