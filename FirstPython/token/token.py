import re;
import ply.lex as lex;

# Specifying Tokens

# Write code for the LANGLESLASH token to match </ in our HTML.

#def t_LANGLESLASH(token):
#    r'</';
#    return token;

# Quoted Strings

# Suppose a string starts with " and ends with " and contains any number of
# characters except ". Write a definition for t_STRING.

# Match Exactly:
#     "cuneiform"
#     "sumerian writing"
# Do Not Match Exactly:
#     "esc \" ape"
#     League of Nations Treaty Series 

#def t_STRING(token):
#    r'"(?:[^"])*"';
#    token.value = token.value[1:-1];
#    return token;

# Whitespace

# Suppose a WORD is any number of characters EXCEPT < > or space. 
# A WORD token should leave its value unchanged.

# Submit a definition for t_WORD.

#def t_WORD(token):
#    r'[^ <>\n]+';
#    return token;

#def t_WHITESPACE(token):
#    r' ';
#    pass;

# Crafting Input

# Define a variable called webpage that holds a string that causes our lexical
# analyzer to produce the exact output below

# LexToken(WORD,'This',1,0)
# LexToken(WORD,'is',1,5)
# LexToken(LANGLE,'<',2,11)
# LexToken(WORD,'b',2,12)
# LexToken(RANGLE,'>',2,13)
# LexToken(WORD,'webpage!',2,14)



#import ply.lex as lex

tokens = ('LANGLE', # <
          'LANGLESLASH', # </
          'RANGLE', # >
          'EQUAL', # =
          'STRING', # "hello"
          'WORD', # Welcome!
          )

states = (
          ('htmlcomment', 'exclusive'),
          );

t_ignore = ' ' # shortcut for whitespace

#HTML comment codes must be at top (first)
def t_htmlcomment(token):
    r'<!--';
    token.lexer.begin('htmlcomment');
    
def t_htmlcomment_end(token):
    r'-->';
    token.lexer.lineno += token.value.count('\n'); #must be in one line
    token.lexer.begin('INITIAL');
    
def t_htmlcomment_error(token):
    token.lexer.skip(1);

def t_newline(token):
    r'\n'
    token.lexer.lineno += 1
    pass

def t_LANGLESLASH(token):
    r'</'
    return token

def t_LANGLE(token):
    r'<'
    return token

def t_RANGLE(token):
    r'>'
    return token

def t_EQUAL(token):
    r'='
    return token

def t_STRING(token):
    r'"[^"]*"'
    token.value = token.value[1:-1]
    return token

def t_WORD(token):
    r'[^ <>\n]+'
    return token


# Identifier

# Identifiers are textual string descriptions that refer to program elements,
# such as variables and functions. Write a indentifier token rule for Javascript identifiers.

# The token rule should match:

#   factorial
#   underscore_separated
#   mystery
#   ABC

# The token rule should not match:

#   _starts_wrong
#   123


def t_IDENTIFIER(token):
    #r'[A-Za-z]+(?:_*[A-Za-z]+)'
    r'[A-Za-z][A-Za-z_]*'
    return token

# Numbers

# Write a indentifier token rule for Javascript numbers that converts the value
# of the token to a float.

# The token rule should match:

#    12
#    5.6
#    -1.
#    3.14159
#    -8.1
#    867.5309

# The token rule should not match:

#    1.2.3.4
#    five
#    jenny

def t_NUMBER(token):
    #r'-?[0-9]+\.?[0-9]*';
    r'-?[0-9]+(?:\.[0-9]*)?';
    token.value = float(token.value);
    return token;

def t_eolcomment(token):
    r'//[^\n]*';
    pass;


webpage = """This is <!-- comment --><b>webpage!"""
htmllexer = lex.lex()
htmllexer.input(webpage)
while True:
    tok = htmllexer.token()
    if not tok: break
    print tok



