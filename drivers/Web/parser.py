import drivers.Web.lexer as lexer

class STATEMENTS:
    def __init__(self, statements: list):
        self.statements = statements

    def __eq__(self, other):
        if not isinstance(other, STATEMENTS):
            return False
        return self.statements == other.statements

    def render(self, context: dict, context_blocks: dict):
        aux = ""
        for statement in self.statements:
            aux += statement.render(context, context_blocks)

        return aux

class STRING_CONSTANT:
    def __init__(self, input_str: str):
        self.input_str = input_str

    def __eq__(self, other):
        if not isinstance(other, STRING_CONSTANT):
            return False
        return self.input_str == other.input_str

    def render(self, context: dict, context_blocks: dict):
        return self.input_str

class IDENTIFIER:
    def __init__(self, var_name: str):
        self.var_name = var_name

    def __eq__(self, other):
        if not isinstance(other, IDENTIFIER):
            return False
        return self.var_name == other.var_name

    def render(self, context: dict, context_blocks: dict):
        return str(context.get(self.var_name, ""))

class EXTENDS:
    def __init__(self, file_name, file_parser):
        self.file_name = file_name
        self.file_parser = file_parser

    def __eq__(self, other):
        if not isinstance(other, EXTENDS):
            return False
        return self.file_name == other.file_name

    def render(self, context: dict, context_blocks: dict):
        return self.file_parser(self.file_name).render(context, context_blocks)

class BLOCK:
    def __init__(self, name: str, content: STATEMENTS):
        self.name = name
        self.content = content

    def __eq__(self, other):
        if not isinstance(other, BLOCK):
            return False
        return self.name == other.name and self.content == other.content

    def render(self, context: dict, context_blocks: dict):
        if self.name in context_blocks and context_blocks[self.name] != self:
            return context_blocks[self.name].render(context, context_blocks)
        return self.content.render(context, context_blocks)

def parser_statements(alexer, template_to_object):
    statements = []
    while True:
        try:
            first_token = alexer.peek()
            if first_token == lexer.BLOCK:
                statements.append(parser_block(alexer, template_to_object))

            elif first_token == lexer.EXTENDS:
                statements.append(parser_extends(alexer, template_to_object))

            elif isinstance(first_token, lexer.IDENTIFIER_CLASS):
                statements.append(parser_identifier(alexer))

            elif isinstance(first_token, lexer.STRING_CONSTANT_CLASS):
                statements.append(parser_string_constant(alexer))

            else:
                break

        except StopIteration:
            break

    return STATEMENTS(statements)

def parser_block(alexer, template_to_object):
    next(alexer)
    block_name = next(alexer).input_str
    block_content = parser_statements(alexer, template_to_object)
    next(alexer)
    return BLOCK(block_name, block_content)

def parser_identifier(alexer):
    identifier = next(alexer)
    return IDENTIFIER(identifier.var_name)

def parser_string_constant(alexer):
    string_constant = next(alexer)
    return STRING_CONSTANT(string_constant.input_str)

def parser_extends(alexer, template_to_object):
    next(alexer)
    extends = next(alexer)
    return EXTENDS(extends.input_str, template_to_object)

class base_template:
    def __init__(self, statements: STATEMENTS):
        self.statements = statements

    def render(self, context: dict, context_blocks: dict):
        return self.statements.render(context, context_blocks)

class child_template:
    def __init__(self, statements: STATEMENTS):
        self.statements = statements

    def render(self, context: dict, context_blocks: dict):
        extends = self.statements.statements[0]
        blocks = self.statements.statements[1:]
        c_blocks = {}
        for block in blocks:
            if isinstance(block, BLOCK):
                c_blocks[block.name] = block

        for block_name in context_blocks:
            c_blocks[block_name] = context_blocks[block_name]

        return extends.render(context, c_blocks)

def parser(alexer, lexer_function):
    class empty_template:
        def render(self, context: dict, context_blocks: dict):
            return ""

    def template_to_object(file_name):
        return parser(lexer_function(file_name), lexer_function)

    try:
        if isinstance(alexer.peek(), lexer.EXTENDS_CLASS):
            return child_template(parser_statements(alexer, template_to_object))

        else:
            return base_template(parser_statements(alexer, template_to_object))

    except StopIteration:
        return empty_template()