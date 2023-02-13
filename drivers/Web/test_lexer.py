import pytest

import drivers.Web.lexer as lexer

def test_lexer_END_TOKEN_raising_StopIteration():
    lxer = lexer.lexer("")
    with pytest.raises(StopIteration):
        next(lxer)


def test_lexer_string_no_keys_with_percent():
    lxer = lexer.lexer("string no keys and percent")
    nxt = next(lxer)
    assert isinstance(nxt, lexer.STRING_CONSTANT_CLASS)

def test_lexer_verifying_str_value():
    lxer = lexer.lexer("string no keys and percent")
    nxt = next(lxer)
    assert nxt.input_str == "string no keys and percent"

def test_lexer_block_support_1_next():
    lxer = lexer.lexer("{% block title %} lorem ipsum {% endblock %}")
    lexer_as_list = next(lxer)
    assert lexer_as_list == lexer.BLOCK

def test_lexer_block_support_2_nexts():
    lxer = lexer.lexer("{% block title %} lorem ipsum {% endblock %}")
    next(lxer)
    lexer_as_list = next(lxer)
    assert lexer_as_list.input_str == "title"

def test_lexer_block_support_3_nexts():
    lxer = lexer.lexer("{% block title %} lorem ipsum {% endblock %}")
    next(lxer)
    next(lxer)
    lexer_as_list = next(lxer)
    assert lexer_as_list.input_str == " lorem ipsum "

def test_lexer_block_support_4_nexts():
    lxer = lexer.lexer("{% block title %} lorem ipsum {% endblock %}")
    next(lxer)
    next(lxer)
    next(lxer)
    lexer_as_list = next(lxer)
    assert lexer_as_list == lexer.END_BLOCK

def test_lexer_block_support_using_list_function():
    lxer = lexer.lexer("{% block title %} lorem ipsum {% endblock %}")
    lexer_as_list = list(lxer)
    assert len(lexer_as_list) == 4 and lexer_as_list[0] == lexer.BLOCK and lexer_as_list[1].input_str == "title" \
           and lexer_as_list[2].input_str == " lorem ipsum " and lexer_as_list[3] == lexer.END_BLOCK

def test_lexer_identifying_end_block():
    lxer = lexer.lexer("{% endblock %}")
    next(lxer)
    assert lxer.input_str == " %}"

def test_lexer_using_next():
    lxer = lexer.lexer("{% endblock %}")
    nxt = next(lxer)
    assert isinstance(nxt, lexer.END_BLOCK_CLASS)

def test_lexer_string_before_block():
    lxer = lexer.lexer("lorem ipsum {% block title %}{% endblock %}")
    lexer_as_list = list(lxer)
    assert lexer_as_list == [lexer.STRING_CONSTANT_CLASS("lorem ipsum "), lexer.BLOCK, lexer.STRING_CONSTANT_CLASS("title"), lexer.END_BLOCK]

def test_lexer_string_before_block_next1():
    lxer = lexer.lexer("lorem ipsum {% block title %}{% endblock %}")
    nxt1 = next(lxer)
    assert nxt1 == lexer.STRING_CONSTANT_CLASS("lorem ipsum ")

def test_lexer_string_before_block_next2():
    lxer = lexer.lexer("lorem ipsum {% block title %}{% endblock %}")
    next(lxer)
    nxt2 = next(lxer)
    assert nxt2 == lexer.BLOCK

def test_lexer_string_before_block_next3():
    lxer = lexer.lexer("lorem ipsum {% block title %}{% endblock %}")
    next(lxer)
    next(lxer)
    nxt3 = next(lxer)
    assert nxt3 == lexer.STRING_CONSTANT_CLASS("title")

def test_lexer_string_constant_same_object1():
    string_constant_1 = lexer.STRING_CONSTANT_CLASS("lorem ipsum ")
    string_constant_2 = lexer.STRING_CONSTANT_CLASS("lorem ipsum ")
    assert string_constant_1 == string_constant_2

def test_lexer_string_before_block_with_block_content():
    lxer = lexer.lexer("lorem ipsum {% block title %}dolor sit amet{% endblock %}")
    lexer_as_list = list(lxer)
    assert lexer_as_list == [lexer.STRING_CONSTANT_CLASS("lorem ipsum "), lexer.BLOCK, lexer.STRING_CONSTANT_CLASS("title"), lexer.STRING_CONSTANT_CLASS("dolor sit amet"), lexer.END_BLOCK]

def test_lexer_identifying_variable():
    lxer = lexer.lexer("{{ is_authenticated }}")
    lexer_as_list = list(lxer)
    assert lexer_as_list == [lexer.IDENTIFIER_CLASS("is_authenticated")]
