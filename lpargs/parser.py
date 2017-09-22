import re
from os.path import basename, splitext, dirname


class LArgsParserException(Exception):
    pass


def without_extension(text):
    result, _ = splitext(text)
    return result


def extension(text):
    _, result = splitext(text)
    return result


class LArgsParser(object):
    def __init__(self, template, delimiter, begin_bracket, end_bracket):
        self.delimiter = delimiter
        self.template = template
        self.subs_pattern = re.compile("\\"+begin_bracket + r'[^\''+begin_bracket+']*' + "\\"+end_bracket)

    functions = {
        'b': basename,
        'e': without_extension,
        'E': extension,
        'd': dirname,
    }

    def _parse(self, expression, text, text_tokens):
        operations = re.findall(r'(\d+|\w)', expression)
        result = text
        for op in operations:
            if op.isdecimal():
                op = int(op)
                result = text_tokens[op - 1] if op <= len(text_tokens) else ''
            else:
                if op in self.functions:
                    result = self.functions[op](result)
                else:
                    raise LArgsParserException('Invalid operation: {}'.format(op))
        return result
        expr_match = self.expressions_pattern.match(expression)
        if not expr_match:
            raise LArgsParserException("Invalid expression: {}".format(expression))

        t_index, t_basename, t_ext = expr_match.groups()
        if t_index != '':
            t_index = int(t_index)
            if t_index >= len(text_tokens) + 1:
                return ''
            result = text_tokens[t_index - 1]
        else:
            result = text

        if t_basename:
            result = basename(result)

        if t_ext:
            result, _ = splitext(result)
        return result

    def sub(self, text):
        text_tokens = text.split(self.delimiter)

        def repl(match):
            expression = match.group(0)
            return self._parse(expression, text, text_tokens)

        # print(text, ',', self.template)
        # print(self.subs_pattern)
        return self.subs_pattern.sub(repl, self.template)
