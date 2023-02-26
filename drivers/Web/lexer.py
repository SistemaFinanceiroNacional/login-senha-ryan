import logging

logger = logging.getLogger("drivers.Web.lexer")

class STRING_CONSTANT_CLASS:
    def __init__(self, input_str):
        self.input_str = input_str

    def __eq__(self, other):
        if not isinstance(other, STRING_CONSTANT_CLASS):
            return False
        return self.input_str == other.input_str

class BLOCK_CLASS:
    pass

class END_BLOCK_CLASS:
    pass

class IDENTIFIER_CLASS:
    def __init__(self, var_name):
        self.var_name = var_name

    def __eq__(self, other):
        if not isinstance(other, IDENTIFIER_CLASS):
            return False
        return self.var_name == other.var_name

class EXTENDS_CLASS:
    pass


EXTENDS = EXTENDS_CLASS()
END_BLOCK = END_BLOCK_CLASS()
BLOCK = BLOCK_CLASS()


class lexer:
    def __init__(self, input_str):
        self.input_str = input_str
        self.start_command = "{% "
        self.end_command = " %}"
        self.start_identifier = "{{ "
        self.end_identifier = " }}"
        self.initial_state = 0
        self.getting_command = 1
        self.getting_identifier = 2
        self.state = self.initial_state
        self.key_words = {"block": BLOCK, "endblock": END_BLOCK, "extends": EXTENDS}

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.input_str == "":
                raise StopIteration()

            if self.state == self.initial_state and not self.input_str.startswith(self.start_command) and not self.input_str.startswith(self.start_identifier):
                aux = ""
                while not self.input_str.startswith(self.start_command) and not self.input_str.startswith(self.start_identifier) and self.input_str != "":
                    aux += self.input_str[0]
                    self.input_str = self.input_str[1:]

                return STRING_CONSTANT_CLASS(aux)

            elif self.state == self.initial_state and self.input_str.startswith(self.start_command):
                self.state = self.getting_command
                self.input_str = self.input_str[3:]

            elif self.state == self.initial_state and self.input_str.startswith(self.start_identifier):
                self.state = self.getting_identifier
                self.input_str = self.input_str[3:]

            elif self.state == self.getting_identifier and self.input_str.startswith(self.end_identifier):
                self.state = self.initial_state
                self.input_str = self.input_str[3:]

            elif self.state == self.getting_identifier and self.input_str.startswith(" "):
                self.input_str = self.input_str[1:]

            elif self.state == self.getting_identifier and not self.input_str.startswith(" "):
                aux = ""
                while self.input_str != "" and not self.input_str.startswith(" ") and not self.input_str.startswith(self.end_identifier):
                    aux += self.input_str[0]
                    self.input_str = self.input_str[1:]

                return IDENTIFIER_CLASS(aux)

            elif self.state == self.getting_command and self.input_str.startswith(self.end_command):
                self.state = self.initial_state
                self.input_str = self.input_str[3:]

            elif self.state == self.getting_command and self.input_str.startswith(" "):
                self.input_str = self.input_str[1:]

            elif self.state == self.getting_command and not self.input_str.startswith(" "):
                aux = ""
                while self.input_str != "" and not self.input_str.startswith(" ") and not self.input_str.startswith(self.end_command):
                    aux += self.input_str[0]
                    self.input_str = self.input_str[1:]

                if aux in self.key_words:
                    return self.key_words[aux]

                else:
                    return STRING_CONSTANT_CLASS(aux)

class auxiliar_lexer:
    def __init__(self, other_lexer):
        self.lexer = other_lexer
        self.look_ahead = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.look_ahead:
            aux = self.look_ahead
            self.look_ahead = None
            return aux

        else:
            return next(self.lexer)

    def peek(self):
        if self.look_ahead:
            return self.look_ahead

        else:
            self.look_ahead = next(self.lexer)
            return self.look_ahead
