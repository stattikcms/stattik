import markblocks.sly as sly

EOF = 'EOF'
NEWLINE = 'NEWLINE'
SEMICOLON = 'SEMICOLON'
TERMINATOR = 'TERMINATOR'
INDENT = 'INDENT'
DEDENT = 'DEDENT'

def create_token(type, value, lineno, index):
    tok = sly.lex.Token()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    tok.index = index
    tok.end = index + 1
    return tok

# Synthesize a TERMINATOR tag
def TERMINATOR_(lineno, index):
    return create_token(TERMINATOR, None, lineno, index)

# Synthesize an INDENT tag
def INDENT_(lineno, index):
    return create_token(INDENT, None, lineno, index)
    
# Synthesize a DEDENT tag
def DEDENT_(lineno, index):
    return create_token(DEDENT, None, lineno, index)
