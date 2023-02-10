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


END_BLOCK = END_BLOCK_CLASS()
BLOCK = BLOCK_CLASS()


class lexer:
    def __init__(self, input_str):
        self.input_str = input_str
        self.start_command = "{% "
        self.end_command = " %}"
        self.buffer = []
        self.initial_state = 0
        self.waiting_command = 1
        self.getting_command = 2
        self.state = self.initial_state

    def __iter__(self):
        return self

    def __next__(self):
        if self.buffer:
            first_element = self.buffer[0]
            self.buffer = self.buffer[1:]
            return first_element

        if self.input_str == "":
            raise StopIteration()

        elif self.input_str.startswith(self.start_command):
            self.buffer = self.process_command()

        else:
            self.buffer = self.process_constant_string()

        first_element = self.buffer[0]
        self.buffer = self.buffer[1:]
        return first_element

    def process_command(self):
        first_close_keys = self.input_str.find("%}")
        block_name_and_type = self.input_str[3:first_close_keys-1].split(" ")

        self.input_str = self.input_str[first_close_keys+1:]

        if block_name_and_type[0] == "endblock":
            self.input_str = ""
            return [END_BLOCK]

        elif block_name_and_type[0] == "block":
            block_name = block_name_and_type[1]

            index_of_block_content = self.input_str.find("{%")
            block_content = self.input_str[1:index_of_block_content]

            self.input_str = ""

            if block_content == "":
                return [BLOCK, STRING_CONSTANT_CLASS(block_name), END_BLOCK]
            return [BLOCK, STRING_CONSTANT_CLASS(block_name), STRING_CONSTANT_CLASS(block_content), END_BLOCK]

    def process_constant_string(self):
        input_str_token = self.input_str
        logger.debug(f"Input_str_token: {input_str_token}")
        index_of_str_constant = self.input_str.find(self.start_command)
        logger.debug(f"Index_of_str_constant: {index_of_str_constant}")
        if index_of_str_constant != -1:
            input_str_token = input_str_token[:index_of_str_constant]
            logger.debug(f"Input_str_token after change: {input_str_token}")
            self.input_str = self.input_str[index_of_str_constant:]
            logger.debug(f"Input_str after change: {self.input_str}")

        return [STRING_CONSTANT_CLASS(input_str_token)]
