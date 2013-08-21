# Parsing JavaScript Statements
#
#
# In this exercise you will write a Parser for a subset of JavaScript. This
# will invole writing parsing rewrite rules (i.e., encoding a context-free
# grammar) and building up a parse tree (also called a syntax tree) of the
# result. 
#
# We have split the parsing of JavaScript into two exercises so that you
# have a chance to demonstrate your mastery of the concepts independently
# (i.e., so that you can get one of them right even if the other proves
# difficult). We could easily make a full JavaScript parser by putting all
# of the rules together. 
#
# In the first part, we will handle JavaScript elements and statements. The
# JavaScript tokens we use will be the same ones we defined together in
# the Homework for Unit 2. (Even if you did not complete Homework 2, the
# correct tokens will be provided here.) 
#
# Let's walk through our JavaScript grammar. We'll describe it somewhat
# informally in text: your job for this homework problem is to translate
# this description into a valid parser!
# 
# The starting non-terminal is "js" for "JavaScript program" -- which is
# just a list of "elements" (to be defined shortly). The parse tree you
# must return is simply a list containing all of the elements.  
#
#       js -> element js
#       js -> 
#
# An element is either a function declaration: 
#
#       element -> FUNCTION IDENTIFIER ( optparams ) compoundstmt
#
# or a statement following by a semi-colon: 
#
#       element -> stmt ; 
#       
# The parse tree for the former is the tuple ("function",name,args,body),
# the parse tree for the latter is the tuple ("stmt",stmt). 
#
#       optparams ->
#       optparams -> params
#       params -> IDENTIFIER , params
#       params -> IDENTIFIER
#
# optparams is a comma-separated list of zero or more identifiers. The
# parse tree for optparams is the list of all of the identifiers. 
#
#       compoundstmt -> { statements } 
#       statements -> stmt ; statements
#       statements -> 
#
# A compound statement is a list of zero or more statements, each of which
# is followed by a semicolon. (In real JavaScript, some statements do not
# need to be followed by a semicolon. For simplicity, we will assume that
# they all have to.) The parse tree for a compound statement is just the
# list of all of the statements. 
#
# We will consider six kinds of possible statements: 
#
#       stmt -> IF exp compoundstmt     
#       stmt -> IF exp compoundstmt ELSE compoundstmt
#       stmt -> IDENTIFIER = exp 
#       stmt -> RETURN exp 
#
# The "if", "assignment" and "return" statements should be familiar. It is
# also possible to use "var" statements in JavaScript to introduce new
# local variables (this is not necessary in Python): 
#
#       stmt -> VAR IDENTIFIER = exp 
#
# And it is also possible to treat an expression as a statement. This is
#
#       stmt -> exp 
#
# The parse trees for statements are all tuples:
#       ("if-then", conditional, then_branch)
#       ("if-then-else", conditional, then_branch, else_branch)
#       ("assign", identifier, new_value) 
#       ("return", expression)
#       ("var", identifier, initial_value) 
#       ("exp", expression) 
#
# To simplify things, for now we will assume that there is only one type of
# expression: identifiers that reference variables. In the next assignment,
# we'll encoding the parsing rules for expressions.
#
# Recall the names of our tokens: 
#
# 'ANDAND',       # &&          | 'LT',           # <
# 'COMMA',        # ,           | 'MINUS',        # -
# 'DIVIDE',       # /           | 'NOT',          # !
# 'ELSE',         # else        | 'NUMBER',       # 1234 
# 'EQUAL',        # =           | 'OROR',         # ||
# 'EQUALEQUAL',   # ==          | 'PLUS',         # +
# 'FALSE',        # FALSE       | 'RBRACE',       # }
# 'FUNCTION',     # function    | 'RETURN',       # return
# 'GE',           # >=          | 'RPAREN',       # )
# 'GT',           # >           | 'SEMICOLON',    # ;
# 'IDENTIFIER',   # factorial   | 'STRING',       # "hello"
# 'IF',           # if          | 'TIMES',        # *
# 'LBRACE',       # {           | 'TRUE',         # TRUE
# 'LE',           # <=          | 'VAR',          # var 
# 'LPAREN',       # (           |
import ply.yacc as yacc
import ply.lex as lex
import jstokens                 # use our JavaScript lexer
from jstokens import tokens     # use out JavaScript tokens

start = 'js'    # the start symbol in our grammar

precedence = (
        # Fill in the precedence and associativity. List the operators
        # in order of _increasing_ precedence (start low, go to high). 
    ('left', 'OROR'), 
    ('left', 'ANDAND'), 
    ('left', 'EQUALEQUAL'), 
    ('left', 'LT', 'LE', 'GT', 'GE'), 
    ('left', 'PLUS', 'MINUS'), 
    ('left', 'TIMES', 'DIVIDE'), 
    ('right', 'NOT'),        
)

def p_js(p): 
    'js : element js'
    p[0] = [p[1]] + p[2]

def p_js_empty(p):
    'js : '
    p[0] = [ ]

######################################################################
# Fill in the rest of the grammar for elements and statements here.
# This can be done in about 50 lines with 15 grammar rules.
######################################################################


# element -> FUNCTION IDENTIFIER ( optparams ) compoundstmt
# element -> stmt ; 
# The parse tree for the former is the tuple ("function",name,args,body),
# the parse tree for the latter is the tuple ("stmt",stmt). 

def p_js_element_function(p):
    'element : FUNCTION IDENTIFIER LPAREN optparams RPAREN compoundstmt';
    p[0] = ('function', p[2], p[4], p[6]);
    
def p_js_element_stmt(p):
    'element : stmt SEMICOLON ';
    p[0] = ('stmt', p[1]);


# optparams ->
# optparams -> params
# params -> IDENTIFIER , params
# params -> IDENTIFIER
# The parse tree for optparams is the list of all of the identifiers. 

def p_js_optparams_empty(p):
    'optparams : ';
    p[0] = [];
    
def p_js_optparams(p):
    'optparams : params';
    p[0] = p[1];
    
def p_js_optparams_params(p):
    'params : IDENTIFIER COMMA params'
    p[0] = [p[1]] + p[3];
    
def p_js_optparams_param(p):
    'params : IDENTIFIER';
    p[0] = [p[1]];

# compoundstmt -> { statements } 
# statements -> stmt ; statements
# statements -> 
#
# A compound statement is a list of zero or more statements, each of which
# is followed by a semicolon. (In real JavaScript, some statements do not
# need to be followed by a semicolon. For simplicity, we will assume that
# they all have to.) The parse tree for a compound statement is just the
# list of all of the statements. 

def p_js_compoundstmt(p):
    'compoundstmt : LBRACE statements RBRACE ';
    p[0] = p[2];
    
def p_js_statements(p):
    'statements : stmt SEMICOLON statements';
    p[0] = [p[1]] + p[3];
    
def p_js_statements_empty(p):
    'statements : ';
    p[0] = [];
    
#       stmt -> IF exp compoundstmt     
#       stmt -> IF exp compoundstmt ELSE compoundstmt
#       stmt -> IDENTIFIER = exp 
#       stmt -> RETURN exp 
#
# The "if", "assignment" and "return" statements should be familiar. It is
# also possible to use "var" statements in JavaScript to introduce new
# local variables (this is not necessary in Python): 
#
#       stmt -> VAR IDENTIFIER = exp 
#
# And it is also possible to treat an expression as a statement. This is
#
#       stmt -> exp 
#
# The parse trees for statements are all tuples:
#       ("if-then", conditional, then_branch)
#       ("if-then-else", conditional, then_branch, else_branch)
#       ("assign", identifier, new_value) 
#       ("return", expression)
#       ("var", identifier, initial_value) 
#       ("exp", expression) 

def p_js_stmt_if(p):
    'stmt : IF exp compoundstmt';
    p[0] = ('if-then', p[2], p[3]);
    
def p_js_stmt_if_else(p):
    'stmt : IF exp compoundstmt ELSE compoundstmt';
    p[0] = ('if-then-else', p[2], p[3], p[5]);
    
def p_js_stmt_assign(p):
    'stmt : IDENTIFIER EQUAL exp';
    p[0] = ('assign', p[1], p[3]);
    
def p_js_stmt_return(p):
    'stmt : RETURN exp';
    p[0] = ('return', p[2]);
    
def p_js_stmt_var(p):
    'stmt : VAR IDENTIFIER EQUAL exp ';
    p[0] = ('var', p[2], p[4]);
    
def p_js_stmt_exp(p):
    'stmt : exp';
    p[0] = ('exp', p[1]);

######################################################################
# While Statement
######################################################################

def p_stmt_while(p):
    'stmt : WHILE exp compoundstmt'
    p[0] = ("while", p[2], p[3])

######################################################################
# done
######################################################################

######################################################################
#
# Included parsing JavaScript Expression
#
######################################################################

# For now, we will assume that there is only one type of expression.
def p_exp_identifier(p): 
    'exp : IDENTIFIER'
    p[0] = ("identifier",p[1]) 
    
# Here's the rules for simple expressions.
        
def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ('number',p[1])

def p_exp_string(p):
    'exp : STRING'
    p[0] = ('string',p[1])
    
def p_exp_true(p):
    'exp : TRUE'
    p[0] = ('true','true')
    
def p_exp_false(p):
    'exp : FALSE'
    p[0] = ('false','false')
    
def p_exp_not(p):
    'exp : NOT exp'
    p[0] = ('not', p[2])
    
def p_exp_parens(p):
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

# This is what the rule for anonymous functions would look like, but since
# they involve statements they are not part of this assignment. Leave this
# commented out, but feel free to use it as a hint.
def p_exp_lambda(p):
    'exp : FUNCTION LPAREN optparams RPAREN compoundstmt'
    p[0] = ("function",p[3],p[5])

######################################################################
# Fill in the rest of the grammar for expressions.
#
# This can be done in about 50 lines using about 12 p_Something()
# definitions. Remember that you can save time by lumping the binary
# operator rules together. 
######################################################################


#    exp ->   exp || exp        # lowest precedence, left associative
#           | exp && exp        # higher precedence, left associative 
#           | exp == exp        # higher precedence, left associative
#           | exp < exp         # /---
#           | exp > exp         # | higher precedence, 
#           | exp <= exp        # | left associative
#           | exp >= exp        # \---
#           | exp + exp         # /--- higher precedence,
#           | exp - exp         # \--- left associative
#           | exp * exp         # /--- higher precedence,
#           | exp / exp         # \--- left associative
#
# In each case, the parse tree is the tuple:
# 
#       ("binop", left_child, operator_token, right_child) 

def p_exp_binary_operation(p):
    '''exp : exp OROR exp
           | exp ANDAND exp
           | exp EQUALEQUAL exp
           | exp LT exp
           | exp GT exp
           | exp LE exp
           | exp GE exp
           | exp PLUS exp
           | exp MINUS exp
           | exp TIMES exp
           | exp DIVIDE exp'''
    p[0] = ('binop', p[1], p[2], p[3]);

# Finally, it is possible to have a function call as an expression:
#
#       exp -> IDENTIFIER ( optargs ) 
#
# The parse tree is the tuple ("call", function_name, arguments). 
#
#       optargs -> 
#       optargs -> args
#       args -> exp , args
#       args -> exp 

def p_exp_function(p):
    'exp : IDENTIFIER LPAREN optargs RPAREN'
    p[0] = ('call', p[1], p[3]);
    
def p_exp_function_optargs_empty(p):
    'optargs : '
    p[0] = [];
    
def p_exp_function_optargs_args(p):
    'optargs : args'
    p[0] = p[1];
    
def p_exp_function_args(p):
    'args : exp COMMA args'
    p[0] = [p[1]] + p[3];
    
def p_exp_function_arg(p):
    'args : exp'
    p[0] = [p[1]];

# We have included a few tests. You will likely want to write your own.

jslexer = lex.lex(module=jstokens) 
jsparser = yacc.yacc() 

def test_parser(input_string): 
    jslexer.input(input_string) 
    parse_tree = jsparser.parse(input_string,lexer=jslexer) 
    return parse_tree

# Simple function with no arguments and a one-statement body.
jstext1 = "function myfun() { return nothing ; }"
jstree1 = [('function', 'myfun', [], [('return', ('identifier', 'nothing'))])]

print test_parser(jstext1) == jstree1

# Function with multiple arguments.
jstext2 = "function nobletruths(dukkha,samudaya,nirodha,gamini) { return buddhism ; }"
jstree2 = [('function', 'nobletruths', ['dukkha', 'samudaya', 'nirodha', 'gamini'], [('return', ('identifier', 'buddhism'))])]
print test_parser(jstext2) == jstree2

# Multiple top-level elemeents, each of which is a var, assignment or
# expression statement. 
jstext3 = """var view = right;
var intention = right;
var speech = right;
action = right;
livelihood = right;
effort_right;
mindfulness_right;
concentration_right;"""
jstree3 = [('stmt', ('var', 'view', ('identifier', 'right'))), ('stmt', ('var', 'intention', ('identifier', 'right'))), ('stmt', ('var', 'speech', ('identifier', 'right'))), ('stmt', ('assign', 'action', ('identifier', 'right'))), ('stmt', ('assign', 'livelihood', ('identifier', 'right'))), ('stmt', ('exp', ('identifier', 'effort_right'))), ('stmt', ('exp', ('identifier', 'mindfulness_right'))), ('stmt', ('exp', ('identifier', 'concentration_right')))]
print test_parser(jstext3) == jstree3

# if-then and if-then-else and compound statements.
jstext4 = """
if cherry {
  orchard;
  if uncle_vanya {
    anton ;
    chekov ;
  } else { 
  } ;
  nineteen_oh_four ;
} ;
"""
jstree4 = [('stmt', ('if-then', ('identifier', 'cherry'), [('exp', ('identifier', 'orchard')), ('if-then-else', ('identifier', 'uncle_vanya'), [('exp', ('identifier', 'anton')), ('exp', ('identifier', 'chekov'))], []), ('exp', ('identifier', 'nineteen_oh_four'))]))]
print test_parser(jstext4) == jstree4

jstext5 = """
    var i = 0;
    while (i <= 5) {
      i = i + 2;
    };
"""
jstree5 = [('stmt', ('var', 'i', ('number', 0.0))), ('stmt', ('while', ('binop', ('identifier', 'i'), '<=', ('number', 5.0)), [('assign', 'i', ('binop', ('identifier', 'i'), '+', ('number', 2.0)))]))]
print (test_parser(jstext5));

jstext6 = """var i = function (x, y) {return 3 + 4;};"""
print (test_parser(jstext6));
