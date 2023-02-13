import drivers.Web.lexer as lexer

class parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def render(self, context: dict):
        try:
            lexer_next = next(self.lexer)

        except StopIteration:
            return ""

        if isinstance(lexer_next, lexer.STRING_CONSTANT_CLASS):
            return lexer_next.input_str

        elif isinstance(lexer_next, lexer.IDENTIFIER_CLASS):
            return str(context.get(lexer_next.var_name))