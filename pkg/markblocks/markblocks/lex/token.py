from dataclasses import dataclass

EOF = 'EOF'
NEWLINE = 'NEWLINE'
SEMICOLON = 'SEMICOLON'
TERMINATOR = 'TERMINATOR'
INDENT = 'INDENT'
DEDENT = 'DEDENT'

@dataclass
class Token:
    type: str
    value: object
    lineno: int = 0
    index: int = 0
    end: int = 0

def create_token(type, value, lineno, index):
    return Token(type, None, lineno, index, index + 1)

# Synthesize a TERMINATOR tag
def TERMINATOR_(lineno, index):
    return create_token(TERMINATOR, None, lineno, index)

# Synthesize an INDENT tag
def INDENT_(lineno, index):
    return create_token(INDENT, None, lineno, index)
    
# Synthesize a DEDENT tag
def DEDENT_(lineno, index):
    return create_token(DEDENT, None, lineno, index)
