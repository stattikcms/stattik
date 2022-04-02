from .lexer import Lexer

class HeadingLexer(Lexer):
    #tokens = { H3, H2, H1 }
    tokens = Lexer.tokens
    fingerprints = [
        (r'(?P<H3>^###( +)?)', 'H3'),
        (r'(?P<H2>^##( +)?)', 'H2'),
        (r'(?P<H1>^#( +)?)', 'H1'),
        (r'(?P<H1U>^==( +)?)', 'H1U'),
        (r'(?P<H2U>^--( +)?)', 'H2U'),
    ]
    def __init__(self):
        super().__init__()

    @_(r'\r?\n+')
    def NEWLINE(self, t):
        return t

    @_(r'###( +)?')
    def H3(self, t):
        return t

    @_(r'##( +)?')
    def H2(self, t):
        return t

    @_(r'--?-+( +)?')
    def H2U(self, t):
        return t

    @_(r'#( +)?')
    def H1(self, t):
        return t

    @_(r'==?=+( +)?')
    def H1U(self, t):
        return t

    @_(r'.+')
    def SPAN(self, t):
        return t
