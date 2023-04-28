# information about user
class User:
    def __init__(self, name, sex, language, second_language, town):
        self.name = name
        self.sex = sex
        self.language = language
        self.secondLanguage = second_language
        self.town = town


client = User("m", "User", "ru", "en", "Минск")
