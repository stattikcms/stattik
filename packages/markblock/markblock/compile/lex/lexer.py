from tkinter.font import ITALIC
import sly

class Lexer(sly.Lexer):

    def __init__(self):
        super().__init__()

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
        TERMINATOR,
        COMMA,
        SEMICOLON,
        INDENT,
        DEDENT,
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
