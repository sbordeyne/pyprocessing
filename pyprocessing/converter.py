import re

import stringcase


def _parse_arg(arg):
    # arg looks like float y=0.0
    if not arg.strip():
        return arg
    print(arg)
    argtype, rest = arg.split(' ', 1)[0]
    argname, *default = arg.split('=')
    if default:
        default = '=' + default[0]
    else:
        default = ''
    if argtype in ('float', 'int', 'bool', 'str'):
        pass
    elif '[]' in argtype:
        argtype = 'list'
    else:
        argtype = ''
    if argtype:
        argtype = f': {argtype}'
    return f'{stringcase.snakecase(argname)}{argtype}{default}'


def _var(match: re.Match) -> str:
    var = match.groupdict()
    return f'{var["varname"]} = {var["value"]}'


def _function(match: re.Match) -> str:
    var = match.groupdict()
    return f'{stringcase.snakecase(var["fname"])}({var["args"]})'


def _function_declaration(match: re.Match) -> str:
    var = match.groupdict()
    rtype = 'None' if var['rtype'] == 'void' else var['rtype']
    fname = var['fname']
    args = [a.strip(' ') for a in var['args'].split(',')]
    args = [_parse_arg(a) for a in args]
    return f'def {fname}({", ".join(args)}) -> {rtype}'


class Converter:
    token_replacements = {
        re.compile(r'//'): '#',  # Comments
        re.compile(r'(^\{|\{$)'): ':',  # Curly braces
        re.compile(r'(^\}|\}$)'): '',
        re.compile(r';( *#.*)?$'): '',  # terminating semicolons
        re.compile(r'(?P<fname>[a-z][a-zA-Z0-9]+)\((?P<args>.*)\)'): _function,
        re.compile((
            r'(?P<rtype>[a-zA-Z]+) (?P<fname>[a-z_]+)'
            r'\((?P<args>[ a-zA-Z0-9_=,]*)\)'
        )): _function_declaration,
        re.compile(
            r'(?P<vartype>\w+) (?P<varname>\w+) ?= ?(?P<value>.+)'
        ): _var,
    }

    @classmethod
    def from_path(cls, path):
        with open(path, 'r') as f:
            return Converter(f.read())

    def __init__(self, sketch):
        self.sketch = sketch.splitlines()

        for pattern, repl in self.token_replacements.items():
            for i, line in enumerate(self.sketch):
                self.sketch[i] = pattern.sub(repl, line)

    def __str__(self):
        return '\n'.join(['from pyprocessing import *', '', ''] + self.sketch)
