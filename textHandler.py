import functions
import json
from fuzzywuzzy import fuzz, process


class TextHandler:
    def __init__(self, commands_file='commands.json'):
        with open(commands_file, 'r', encoding="utf-8") as f:
            self.function_map = json.load(f, object_hook=dict)
            f.close()

    def get_best_match(self, word):
        best_score = 0
        best_match = None
        for key, words_list in self.function_map.items():
            for w in words_list:
                score = fuzz.ratio(word.lower(), w.lower())
                if score > best_score:
                    best_score = score
                    best_match = key
        return best_match

    def map_string_to_function(self, input_string: str) -> list:
        words = input_string.split()
        if len(words) == 0:
            function_to_call = getattr(functions, 'default_function')
        else:
            for word in words:
                best_match = self.get_best_match(word)
                if best_match:
                    function_to_call = getattr(
                        functions, best_match + '_function')
                    remaining_words = words.copy()
                    remaining_words.remove(word)
                    remaining_string = ' '.join(remaining_words)
                    if best_match == "stop":
                        return [False, function_to_call(remaining_string)]
                    return [True, function_to_call(remaining_string)]
            function_to_call = getattr(functions, 'default_function')
        return [True, function_to_call(words)]