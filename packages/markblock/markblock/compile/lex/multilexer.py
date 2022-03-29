import re

from .lexer import Lexer
from .token import *

class MultiLexer(Lexer):
    tokens = []
    def __init__(self):
        super().__init__()
        self.lexers = []
        self.lexer_map = {}
        self.fingerprints = []
        self.regex = None
        self.default_lexer = None

    def add_lexer(self, lexer, default=False):
        self.lexers.append(lexer)
        if default:
            self.default_lexer = lexer
            return

        fingerprints = lexer.fingerprints
        self.fingerprints += fingerprints
        for fingerprint in fingerprints:
            if not self.regex:
                self.regex = fingerprint[0]
            else:
                self.regex += r'|' + fingerprint[0]
            self.lexer_map[fingerprint[1]] = lexer

    def tokenize(self, text, lineno=1, index=0):
        print('tokenize')
        tokens = []
        child_tokens = []
        lines = text.splitlines()
        #print(self.regex)
        p = re.compile(self.regex)

        indent_stack = [0]

        for lineno, line in enumerate(lines):
            #print(line)
            lstripped = line.lstrip()
            m = p.match(lstripped)
            #print(m)
            child_tokens = None
            if m:
                #print(m.groupdict())
                for key, val in m.groupdict().items():
                    if val:
                        child_tokens = list(self.lexer_map[key].tokenize(line, lineno+1))
            else:
                child_tokens = list(self.default_lexer.tokenize(line))

            child_indent = len(child_tokens[0].value) if len(child_tokens) and child_tokens[0].type == 'WS' else 0
            if child_tokens and child_tokens[0].type == 'WS':
                child_tokens.pop(0)
            if child_indent > indent_stack[-1]:
                indent_stack.append(child_indent)
                tokens.append(INDENT_(index, child_indent))
            elif child_indent < indent_stack[-1]:
                while child_indent < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(DEDENT_(index, child_indent))

                #indent_stack.pop(-1)
                #tokens.append(DEDENT_(index, child_indent))

            tokens += child_tokens
            #tokens.append(self.create_token(self.NEWLINE, None, lineno, 0))
            tokens.append(TERMINATOR_(index, child_indent))


        while len(indent_stack) > 1:
            child_indent = indent_stack.pop()
            tokens.append(DEDENT_(index, child_indent))
                
        result = []
        span = None
        for token in tokens:
            if token.type != 'SPAN':
                if not span:
                    result.append(token)
                else:
                    result.append(span)
                    result.append(token)
                    span = None
                continue
            else:
                if not span:
                    span = token
                else:
                    span.value += token.value

        return result

