import functions
import json


class TextHandler:
    def __init__(self, commands_file='commands.json'):
        with open(commands_file, 'r', encoding="utf-8") as f:
            self.function_map = json.load(f, object_hook=dict)
            f.close()

    # Возвращает функци
    def map_string_to_function(self, input_string: str) -> [bool, str]:
        words = input_string.split()
        if len(words) == 0:
            function_to_call = getattr(functions, 'default_function')
        else:
            first_word = words[0].lower()
            for variants in self.function_map.items():
                if first_word in variants[1]:
                    function_to_call = getattr(functions, variants[0] + '_function')
                    if variants[0] == "stop":
                        return [False, function_to_call(words[1:])]
                    return [True, function_to_call(words[1:])]
            function_to_call = getattr(functions, 'default_function')
        return [True, function_to_call(words[1:])]
