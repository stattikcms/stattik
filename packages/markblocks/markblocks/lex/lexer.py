from tkinter.font import ITALIC
import sly

class Lexer(sly.Lexer):

    def __init__(self):
        super().__init__()

    def error(self, t):
        #print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        print(f"{self.__class__.__name__}: Line {self.lineno}: Bad character '{t.value[0]}'")
        self.index += 1

    def create_token(self, type, value, lineno, index):
        tok = sly.lex.Token()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        tok.index = index
        return tok


    tokens = {
        INDENT,
        DEDENT,
        COMMENT,
        WS,
        NEWLINE,
        NAME,
        STRING,
        TERMINATOR,
        COMMA,
        SEMICOLON,
        EOF,

        SPAN,
        TAG,
        H1,
        H2,
        H3,
        H1U,
        H2U,
        BOLD,
        ITALIC,
        BOLDITALIC,
        BLOCKQUOTE,
        UL,
        OL,
        FENCE,
        ADMONITION,

        IMPORT,
        INSTANCEOF,
        HALT,
        PROPERTY,
        CODE,
        SIG,
        TRUE,
        FALSE,
        NOT,
        AMP,
        BANG,
        SLASH,
        STAR,
        DCOLON,
        TYPE,
        POSTTYPE,
        WHERE,
        CLASS,
        PREDICATE,
        DEF,
        IF,
        VARIABLE,
        VERB,
        NOUN,
        NUMBER,  # Python decimals
        SNIPPET,
        STRING,  # single quoted strings only; syntax of raw strings
        LPAR,
        RPAR,
        NLONGARROW,  #!-->
        LONGARROW,  # -->
        NARROW,  #!->
        ARROW,  # ->
        NLONGFATARROW,  #!==>
        LONGFATARROW,  # ==>
        NFATARROW,  #!=>
        FATARROW,  # =>
        GRAVE,
        CARET,
        COLON,
        DBLCOLON,
        LTCOLON,
        LTLTCOLON,
        AT,
        EQ,
        EQEQ,
        NEQ,
        ASSIGN,
        LT,
        GT,
        PLUS,
        MINUS,
        MINUSPLUS,
        MULT,
        DIV,
        RETURN,
    }

    # Whitespace
    #@_(r' [ \t]+ ')
    @_(r'^ +')
    def WS(self, t):
        return t
