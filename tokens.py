import ply.lex as lex

# List of token names. This is always required
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'SEMICOLON'
]

# Reserved words
reserved = {
    'int': 'INT',
    'return': 'RETURN'
}

# Add reserved words to tokens list
tokens += reserved.values()

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to a python integer
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
int main() {
    int a = 10;
    int b = 20;
    int sum = a + b;
    return sum;
}
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
