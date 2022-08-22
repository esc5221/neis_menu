import re

class DishFormatter():
    compiled_regex1 = re.compile(r'\*{1,2}|\({0,1}\d{1,2}\.\){0,1}|\s{2,}')
    compiled_regex2 = re.compile(r'<br\/>')

    @classmethod
    def format_raw_str(cls, dishes):
        regex_1 = cls.compiled_regex1
        regex_2 = cls.compiled_regex2
        replaced = regex_1.sub('', dishes)
        replaced = regex_2.sub(', ', replaced)
        return replaced