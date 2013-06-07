# JavaScript: Numbers & Strings
# 
# In this exercise you will finish out the token definitions for JavaScript 
# by handling Numbers, Identifiers and Strings. 
#
# We have split the lexing of JavaScript into two exercises so that
# you have a chance to demonstrate your mastery of the concepts
# independently (i.e., so that you can get one of them right even if the
# other proves difficult). We could easily make a full JavaScript lexer by
# putting all of the rules together. 
#
# For this assignment, a JavaScript IDENTIFIER must start with an upper- or
# lower-case character. It can then contain any number of upper- or
# lower-case characters or underscores. Its token.value is the textual
# string of the identifier. 
#       Yes:    my_age
#       Yes:    cRaZy
#       No:     _starts_with_underscore
#
# For this assignment, a JavaScript NUMBER is one or more digits. A NUMBER
# can start with an optional negative sign. A NUMBER can contain a decimal
# point, which can then be followed by zero or more additional digits. Do
# not worry about hexadecimal (only base 10 is allowed in this problem).
# The token.value of a NUMBER is its floating point value (NOT a string).
#       Yes:    123
#       Yes:    -456
#       Yes:    78.9
#       Yes:    10.
#       No:     +5
#       No:     1.2.3
#
# For this assignment, a JavaScript STRING is zero or more characters
# contained in double quotes. A STRING may contain escaped characters.
# Notably, \" does not end a string. The token.value of a STRING is
# its contents (not including the outer double quotes). 
#       Yes:    "hello world"
#       Yes:    "this has \"escaped quotes\""
#       No:     "no"t one string" 
#
# Hint: float("2.3") = 2.3

import ply.lex as lex

tokens = (
        'IDENTIFIER',   
        'NUMBER',       
        'STRING',       
)

#
# Write your code here. 
#


t_ignore                = ' \t\v\r' # whitespace 

def t_IDENTIFIER(token):
    r'[A-Za-z]+(?:_*[A-Za-z]+)*'
    token.type = 'IDENTIFIER';
    return token;

def t_NUMBER(token):
    r'-?[0-9]+(?:\.[0-9]*)?';
    token.value = float(token.value);
    return token;

def t_STRING(token):
    r'"(?:[^"\\]|(?:\\.))*"'
    token.value = token.value[1:-1];
    return token;

def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

def t_error(t):
        print "JavaScript Lexer: Illegal character " + t.value[0]
        t.lexer.skip(1)

# We have included two test cases to help you debug your lexer. You will
# probably want to write some of your own. 

lexer = lex.lex() 

def test_lexer(input_string):
    lexer.input(input_string)
    result = [ ] 
    while True:
        tok = lexer.token()
        if not tok: break
        result = result + [tok.type,tok.value]
    return result

input1 = 'some_identifier -12.34 "a \\"escape\\" b"'
output1 = ['IDENTIFIER', 'some_identifier', 'NUMBER', -12.34, 'STRING', 
'a \\"escape\\" b']
#print test_lexer(input1) == output1
#print (test_lexer(input1))


input2 = '-12x34' 
output2 = ['NUMBER', -12.0, 'IDENTIFIER', 'x', 'NUMBER', 34.0]
#print test_lexer(input2) == output2
#print (test_lexer(input2))

# Euclid's Algorithm
#
# Format: Submit JavaScript Code
#
# In mathematics, because 8 divides 24 evenly, we say that 8 is a
# *divisor* of 24. When computing, it is often useful to find the
# largest divisor that two numbers have in common. For example, 36
# and 24 are both divisible by 2, 3, 4, and 12: the greatest
# divisor that they have in common is 12. It turns out that finding
# common divisors for numbers is critical for modern cryptography,
# including public-key crypto systems such as RSA: a backbone of internet
# commerce. 
#
# Perhaps the oldest algorithm known -- ever! -- is for computing the
# greatest common divisor of two positive numbers. It is attributed to the
# Greek mathematician Euclid around 300 BCE. Here's how it goes: 
#
# You are computing the greatest common divisor ("gcd") of two positive
# integers called "a" and "b". The gcd can be computed recursively (or
# iteratively) using the following three rules: 
#
#       gcd(a,b) = a                    if a == b
#       gcd(a,b) = gcd(a-b,b)           if a > b
#       gcd(a,b) = gcd(a,b-a)           if a < b 
#
# Write a JavaScript (_not_ Python) program that declares a function called gcd
# that accepts two positive integer arguments a and b and returns their greatest
# common divisor. Store your function in a variable called javascriptcode.
#
# We will return anything printed out when you hit submit as we execute the
# JavaScript behind the scenes.

javascriptcode="""
function gcd(a,b) {
    //Write Code Here
}

write( gcd(24,8) == 8 ); 
write(" ");
write( gcd(1362, 1407) ); // Empress Xu (Ming Dynasty) wrote biographies
write(" ");
write( gcd(1875, 1907) ); // Qiu Jin, feminist, revolutionary, and writer
write(" ");
write( gcd(45,116) ); // Ban Zhao, first known female Chinese historian
"""

def gcd(a, b):
    if a == b:
        return a;
    if a > b:
        return gcd(a - b, b);
    else:
        return gcd(a, b - a);
    
def gcd_m(a, b):
    if b == 0:
        return a;
    else:
        return gcd_m(b, a % b);
    
def gcd_l(a, b):
    while a != b:
        if a > b:
            a = a - b;
        else:
            b = b - a;
    return a;
    
#print (gcd(24, 8));
#print (gcd_m(24, 8));
#print (gcd_l(24, 8));

# Title: FSM Optimization
# 
# Challenge Problem: 2 Stars
#
# Lexical analyzers are implemented using finite state machines generated
# from the regular expressions of token definition rules. The performance
# of a lexical analyzer can depend on the size of the resulting finite
# state machine. If the finite state machine will be used over and over
# again (e.g., to analyze every token on every web page you visit!), we
# would like it to be as small as possible (e.g., so that your webpages
# load quickly). However, correctness is more important than speed: even
# an optimized FSM must always produce the right answer.  
#
# One way to improve the performance of a finite state machine is to make
# it smaller by removing unreachable states. If such states are removed,
# the resulting FSM takes up less memory, which may make it load faster or
# fit better in a storage-constrained mobile device.
#
# For this assignment, you will write a procedure nfsmtrim that removes
# "dead" states from a non-deterministic finite state machine. A state is
# (transitively) "dead" if it is non-accepting and only non-accepting
# states are reachable from it. Such states are also called "trap" states:
# once entered, there is no escape. In this example FSM for r"a*" ...
#
# edges = { (1,'a') : [1] ,
#           (1,'b') : [2] ,
#           (2,'b') : [3] ,
#           (3,'b') : [4] } 
# accepting = [ 1 ] 
# 
# ... states 2, 3 and 4 are "dead": although you can transition from 1->2,
# 2->3 and 3->4 on "b", you are doomed to rejection if you do so. 
#
# You may assume that the starting state is always state 1. Your procedure
# nfsmtrim(edges,accepting) should return a tuple (new_edges,new_accepting)
# corresponding to a FSM that accepts exactly the same strings as the input
# FSM but that has all dead states removed. 
#
# Hint 1: This problem is tricky. Do not get discouraged. 
#
# Hint 2: Think back to the nfsmaccepts() procedure from the "Reading
# Machine Minds" homework problem in Unit 1. You are welcome to reuse your
# code (or the solution we went over) to that problem. 
#
# Hint 3: Gather up all of the states in the input machine. Filter down
# to just those states that are "live". new_edges will then be just like
# edges, but including only those transitions that involve live states.
# new_accepting will be just like accepting, but including only those live
# states.

def nfsmaccepts(current, edges, accepting, visited):
    if current in accepting:
        return "";
    if current in visited:
        return None;
    else:
        visited.append(current);
        for edge in edges:
            if current == edge[0]:
                letter = edge[1];
                states = edges[edge];
                for state in states:
                    if state not in visited:
                        r = nfsmaccepts(state, edges, accepting, visited);
                        if r is not None:
                            return letter + r;
        return None;

def add_to_new_edges(new_edges, edge, state):
    if edge in new_edges:
        new_edges[edge].append(state);
    else:
        new_edges[edge] = [state];
        
def reach_to_accepting(start_state, edges, accepting, visited):
    if start_state in accepting:
        return True;
    else:
        visited.append(start_state);
        for edge in edges:
            if start_state == edge[0]:
                for state in edges[edge]:
                    if state not in visited:
                        if reach_to_accepting(state, edges, accepting, visited):
                            return True;
        return False;
         
def create_new_edges(edges, accepting):
    new_edges = {}
    live_states = [];
    for edge in edges:
        for state in edges[edge]:
            if reach_to_accepting(state, edges, accepting, []):
                add_to_new_edges(new_edges, edge, state);
                live_states.append(state);
    return new_edges, live_states;
                

def nfsmtrim(edges, accepting):
    new_edges, live_states = create_new_edges(edges, accepting);
    new_accepting = [];
    for st in accepting:
        if st in live_states:
            new_accepting.append(st);
    return (new_edges, new_accepting);


# We have included a few test cases, but you will definitely want to make
# your own. 

edges1 = { (1,'a') : [1] ,
           (1,'b') : [2] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (8,'z') : [9] , } 
accepting1 = [ 1 ] 
(new_edges1, new_accepting1) = nfsmtrim(edges1,accepting1) 
print new_edges1 == {(1, 'a'): [1]}
print new_accepting1 == [1] 

(new_edges2, new_accepting2) = nfsmtrim(edges1,[]) 
print new_edges2 == {}
print new_accepting2 == [] 

(new_edges3, new_accepting3) = nfsmtrim(edges1,[3,6]) 
print new_edges3 == {(1, 'a'): [1], (1, 'b'): [2], (2, 'b'): [3]}
print new_accepting3 == [3]

print (new_edges3)
print (new_accepting3)

edges4 = { (1,'a') : [1] ,
           (1,'b') : [2,5] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (3,'c') : [2,1,4] } 
accepting4 = [ 2 ] 
(new_edges4, new_accepting4) = nfsmtrim(edges4, accepting4) 
print new_edges4 == { 
  (1, 'a'): [1],
  (1, 'b'): [2], 
  (2, 'b'): [3], 
  (3, 'c'): [2, 1], 
}
print new_accepting4 == [2]

edges3 = {(1, 'a'): [1], (1, 'b'): [2], (2, 'b'): [3]};
accepting3 = [3];
new_edges = {}

edges4 =  { (1, 'a'): [1],
  (1, 'b'): [2], 
  (2, 'b'): [3], 
  (3, 'c'): [2, 1], 
}
accepting4 = [ 2 ] 

edges5 = { (1,'a') : [1] ,
           (1,'b') : [2,5] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (3,'c') : [2,1,4] } 
accepting5 = [ 2 ] 
#create_new_edges(1, edges3, accepting3, [], new_edges);
#print (new_edges);
#print (reach_to_accepting(4, edges5, accepting5, []));
#print (create_new_edges(edges5, accepting5));
#temp = create_new_edges(edges5, accepting5);
#(new_edges4, new_accepting4) = nfsmtrim(edges5, accepting5) 
#print ([s for e, s in edges5.items()]);
#r = [];
#for e, s in edges5.items():
#    r = r + s;
#print r;
#print (temp == edges4);
#print (create_new_edges(edges1, []));