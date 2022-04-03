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
        self.fence_stack = []

    @property
    def fence(self):
        return self.fence_stack[-1]

    def push_fence(self, fence):
        fence.value = ''
        self.fence_stack.append(fence)

    def pop_fence(self):
        return self.fence_stack.pop(-1)

    def in_fence(self):
        return len(self.fence_stack) > 0
        
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
        tokens = []
        child_tokens = []
        lines = text.splitlines()
        #print(self.regex)
        p = re.compile(self.regex)

        indent_stack = [0]
        indent = 0

        for lineno, rawline in enumerate(lines):
            #print(line)
            line = rawline.lstrip()
            indent = len(rawline) - len(line)
            m = p.match(line)
            #print(m)
            child_tokens = None
            if m:
                #print(m.groupdict())
                for key, val in m.groupdict().items():
                    if val:
                        child_tokens = list(self.lexer_map[key].tokenize(line, lineno+1))
            else:
                child_tokens = list(self.default_lexer.tokenize(line))

            if child_tokens and child_tokens[0].type == 'FENCE':
                if self.in_fence():
                    fence = self.pop_fence()
                    #print(fence.value)
                    continue
                else:
                    self.push_fence(child_tokens[0])
            elif self.in_fence():
                self.fence.value += f"{rawline}\n"
                continue

            if indent > indent_stack[-1]:
                indent_stack.append(indent)
                tokens.append(INDENT_(index, indent))
            elif indent < indent_stack[-1] and child_tokens and child_tokens[0].type != 'TERMINATOR' and child_tokens[0].index != 0:
                while indent < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(DEDENT_(index, indent))

            tokens += child_tokens
            tokens.append(TERMINATOR_(index, indent))


        while len(indent_stack) > 1:
            indent = indent_stack.pop()
            tokens.append(DEDENT_(index, indent))
                
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

