import re;

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


webpage = """This is
   <b>webpage!"""



#import ply.lex as lex

tokens = ('LANGLE', # <
          'LANGLESLASH', # </
          'RANGLE', # >
          'EQUAL', # =
          'STRING', # "hello"
          'WORD', # Welcome!
          )

t_ignore = ' ' # shortcut for whitespace

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



#htmllexer = lex.lex()
#htmllexer.input(webpage)
#while True:
#    tok = htmllexer.token()
#    if not tok: break
#    print tok



