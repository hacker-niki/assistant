class TextHandler:
    input_string: str = ""

    def __init__(self, commands_file='commands.json'):
        with open(commands_file, 'r') as f:
            self.function_map = json.load(f)

    def map_string_to_function(self):
        words = self.input_string.split()
        first_word = words[0].lower()

        for command, variants in self.function_map.items():
            if first_word in variants:
                function_to_call = getattr(functions, command + '_function')
                return function_to_call(words[1:])

        function_to_call = getattr(functions, 'default_function')
        return function_to_call(words[1:])

    def set_input_string(self, input_string):
        self.input_string = input_string
