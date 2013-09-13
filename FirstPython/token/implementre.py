# Implementing RE
# Challenge Problem 
#
# Focus: All Units
#
#
# In this problem you will write a lexer, parser and interpreter for
# strings representing regular expressions. Your program will output 
# a non-deterministic finite state machine that accepts the same language
# as that regular expression. 
#
# For example, on input 
#
# ab*c
#
# Your program might output
# 
# edges = { (1,'a')  : [ 2 ] ,
#           (2,None) : [ 3 ] ,    # epsilon transition
#           (2,'b')  : [ 2 ] ,
#           (3,'c')  : [ 4 ] } 
# accepting = [4]
# start = 1
#
# We will consider the following regular expressions:
#
#       single characters       #       a       
#       regexp1 regexp2         #       ab
#       regexp *                #       a*
#       regexp1 | regexp2       #       a|b
#       ( regexp )              #       (a|b)* -- same as (?:a|b) 
#
# That's it. We won't consider [a-c] because it's just a|b|c, and we won't
# consider a+ because it's just aa*. We will not worry about escape
# sequences. Single character can be a-z, A-Z or 0-9 -- that's it. No need
# to worry about strange character encodings. We'll use ( ) for regular
# expression grouping instead of (?: ) just to make the problem simpler.
#
# Don't worry about precedence or associativity. We'll fully parenthesize
# all regular expressions before giving them to you. 
#
# You will write a procedure re_to_nfsm(re_string). It takes as input a
# single argument -- a string representing a regular expression. It returns
# a tuple (edges,accepting,start) corresponding to an NSFM that accepts the
# same language as that regular expression.
#
# Hint: Make a lexer and a paser and an interpreter. Your interpreter may
# find it handy to know the current state and the goal state. Make up as
# many new states as you need. 
# 
import ply.lex as lex
import ply.yacc as yacc

# Fill in your code here. 

tokens= (
         "LETTER",      # a b c
         "OR",          # |
         "LPAREN",      # (
         "RPAREN",      # )
         "ZEROMORE",    # *
         );
         
t_ignore = ' \t\v\r'

def t_error(t):
    print "Regular Expression Lexer: Illegal character " + t.value[0];
    t.lexer.skip(1);
    
def t_LETTER(t):
    r'[a-zA-Z]'
    return t;

def t_OR(t):
    r'\|'
    return t;

def t_LPAREN(t):
    r'\('
    return t;

def t_RPAREN(t):
    r'\)'
    return t;

def t_ZEROMORE(t):
    r'\*'
    return t;
         
start = 'regexp'    # the start symbol in our grammar

precedence = (
              ("left", "OR"),
              #("left", "CONCAT"),
              ("left", "ZEROMORE"),
              )

def p_error(p):
    raise SyntaxError

def p_regexp(p):
    'regexp : exp'
    p[0] = p[1];

def p_regexp_empty(p):
    'regexp : '
    p[0] = [];
    
def p_regexp_regexp(p):
    'exp : LETTER'
    p[0] = [("letter", p[1])];
    
def p_regexp_regexps(p):
    'exp : exp exp'
    p[0] = p[1] + p[2];
    
def p_regexp_zeromore(p):
    'exp : exp ZEROMORE'
    p[0] = [("zeromore", p[1])];
    
def p_regexp_parens_group(p):
    'exp : LPAREN exp RPAREN'
    p[0] =  [("group", p[2])];
    
def p_regexp_or(p):
    'exp : exp1 OR exp2'
    p[0] = [("or", p[1], p[3])];
    
def p_regexp_exp1(p):
    'exp1 : exp'
    p[0] = p[1];
    
def p_regexp_exp2(p):
    'exp2 : exp'
    p[0] = p[1];
    
#
# Interpret feature 
#   
def update_edges(edges, edge, n_state):
    if edge in edges:
        edges[edge].append(n_state);
    else:
        edges[edge] = [n_state];
        
def update_env(env, key, value):
    env[key] = value;
    
def lookup_env(env, key):
    if key in env:
        return env[key];
    return None;

def track_regexp(env, op):
    if "regexpop" in env:
        env["regexpop"].append(op);
    else:
        env["regexpop"] = [op];
        
def lookup_last_regexp(env):
    if "regexpop" in env and env["regexpop"]:
        return env["regexpop"][-1];
    return None;

def close_last_regexp(env):
    if "regexpop" in env and env["regexpop"]:
        return env["regexpop"].pop();
        
def eval_regexp(exp, edges, start, current, accept, lastelt, regexpor, zeromore, group, env):
    etype = exp[0];
    
    print "eval regexp '%s' value '%s'" % (etype, exp[1]);
    print "eval regexp current ", current;
    print "eval regexp start ", start;
    print "eval regexp lastelt ", lastelt;
    
    last_op = lookup_last_regexp(env);
    regexpor, zeromore, group = False, False, False;
    if last_op is not None:
        i = ["or", "zeromore", "group"].index(last_op);
        if i == 0:
            regexpor = True;
        if i == 1:
            zeromore = True;
        if i == 2:
            group = True;
            
    if (regexpor or group) and lookup_env(env, "start") is None:
        update_env(env, "start", current);
        start = current;
    if (regexpor or group) and lastelt:
        update_env(env, "lastgroupelt", True);
        
    if group and lookup_env(env, "ortoinit") and lookup_env(env, "init_or_state") is None:
        update_env(env, "init_or_state", True);
            
    print "eval regexp env ", env;
            
    next_state = current + 1;
    if etype == "letter":
        s_char = exp[1];
        if zeromore:
            edge = (current, None);
            update_edges(edges, edge, next_state);
            edge = (current, s_char);
            update_edges(edges, edge, next_state - 1);
            accept.append(next_state);
        elif group:
            print "see group ";
            if lookup_env(env, "init_or_state"):
                or_start = lookup_env(env, "start");
                edge = (or_start, s_char);
                next_state = current;
                update_env(env, "init_or_state", False);
            else:
                edge = (current, s_char);
                
            if lookup_env(env, "lastgroupelt"):
                group_start = lookup_env(env, "start");
                update_edges(edges, edge, group_start);
                accept.append(group_start);
                update_env(env, "lastgroupelt", False);
            else:
                update_edges(edges, edge, next_state);
                accept.append(next_state);
        elif regexpor:
            if lookup_env(env, "ortoinit"):
                regexpor_start = lookup_env(env, "start");
                edge = (regexpor_start, s_char);
                next_state = current;
                update_env(env, "ortoinit", False);
            else:
                edge = (current, s_char);
                
            print "edge is ", edge;
            
            if lookup_env(env, "lastgroupelt"):
                regexpor_start = lookup_env(env, "start");
                update_edges(edges, edge, regexpor_start);
                accept.append(regexpor_start);
                update_env(env, "lastgroupelt", False);
            else:
                update_edges(edges, edge, next_state);
                accept.append(next_state);                 
        else:
            if lookup_env(env, "lastgroupelt"):
                print "eval current last group elt", current;
                t_cur = current;
                current = lookup_env(env, "start");
                update_env(env, "lastgroupelt", False);
                edge = (current, s_char);
                update_edges(edges, edge, t_cur);
                accept.append(t_cur);
                current = t_cur - 1;
            else:
                if last_op is None and lookup_env(env, "start"):
                    next_state = current;
                    current = lookup_env(env, "start");
                    update_env(env, "start", None);
                edge = (current, s_char);
                update_edges(edges, edge, next_state);
                accept.append(next_state); 
    return next_state;

def eval_regexp_list(elts, edges, start, current, accept, regexpor, zeromore, group, env):
    for count in range(len(elts)):
        lastelt = (count == (len(elts) - 1));
        current = eval_elt(elts[count], edges, start, current, accept, lastelt, regexpor, zeromore, group, env);
    return current;

def eval_elt(elt, edges, start, current, accept, lastelt, regexpor, zeromore, group, env):
    etype = elt[0];
    if elt[0] == "or":
        track_regexp(env, "or");
        lhs = elt[1];
        rhs = elt[2];
        current = eval_regexp_list(lhs, edges, start, current, accept, True, zeromore, group, env);
        update_env(env, "ortoinit", True);
        current = eval_regexp_list(rhs, edges, start, current, accept, True, zeromore, group, env);
        update_env(env, "ortoinit", False);
        close_last_regexp(env);
    elif elt[0] == "group":
        track_regexp(env, "group");
        zhs = elt[1];
        current = eval_regexp_list(zhs, edges, start, current, accept, regexpor, zeromore, True, env);
        update_env(env, "init_or_state", None);
        close_last_regexp(env);
    elif etype == "zeromore":
        track_regexp(env, "zeromore");
        rhs = elt[1];
        current = eval_regexp_list(rhs, edges, start, current, accept, regexpor, True, group, env);
        close_last_regexp(env);
    elif etype == "letter":
        current = eval_regexp(elt, edges, start, current, accept, lastelt, regexpor, zeromore, group, env);
    return current;


#
# Interpret regular express parse tree
#
def interpret(reg_tree):
    edges = {};
    start = 1;
    current = 1;
    accept = [];
    env = {};
    for elt in reg_tree:
        current = eval_elt(elt, edges, start, current, accept, False, False, False, False, env);
    return edges, [accept[-1]], start;




regexplexer = lex.lex() 
parser = yacc.yacc() 

def test_parser(input_string):
    regexplexer.input(input_string);
    result = [ ]
    while True:
        tok = regexplexer.token()
        if not tok: break
        result = result + [tok.type]
    print ("Tokens -> "), result;
    
    parse_tree = parser.parse(input_string, lexer=regexplexer);
    
    print ("Parse tree -> "), parse_tree;
    
    edges = interpret(parse_tree);
    
    return edges;

r = 'a(bx|by)c'
print (test_parser("a(bx|by)c"));

import re;

rg = r'(?:ab)+cde|f'
rg = r'a|a'
#rg = r'a(?:bcde)f'
rg = r'(?:ab)|cd'

print (re.findall(rg, "ababcdefghij bbd "))


#def re_to_nfsm(re_string): 
#        # Feel free to overwrite this with your own code. 
#        lexer.input(re_string)
#        parse_tree = parser.parse(re_string, lexer=lexer) 
        #return interpret(parse_tree) 

# We have included some testing code ... but you really owe it to yourself
# to do some more testing here.

def nfsmaccepts(edges, accepting, current, string, visited): 
        # If we have visited this state before, return false. 
        if (current, string) in visited:
                return False
        visited.append((current, string))       

        # Check all outgoing epsilon transitions (letter == None) from this
        # state. 
        if (current, None) in edges:
                for dest in edges[(current, None)]:
                        if nfsmaccepts(edges, accepting, dest, string, visited):
                                return True

        # If we are out of input characters, check if this is an
        # accepting state. 
        if string == "":
                return current in accepting

        # If we are not out of input characters, try all possible
        # outgoing transitions labeled with the next character. 
        letter = string[0]
        rest = string[1:]
        if (current, letter) in edges:
                for dest in edges[(current, letter)]:
                        if nfsmaccepts(edges, accepting, dest, rest, visited):
                                return True
        return False
    
print ("testing.......")
edges = {(4, 'd'): [5], (5, 'e'): [6], (1, 'a'): [2], (2, 'b'): [3], (3, 'c'): [4]}
edges = {(2, 'f'): [4], (1, 'a'): [2], (4, 'e'): [5], (2, 'b'): [3], (3, 'c'): [2]}
edges = {(1, 'a'): [2], (3, 'x'): [2], (2, 'b'): [3, 4], (2, 'c'): [5], (4, 'y'): [2]}
#print nfsmaccepts(edges, [6], 1, "abcde", []);
print nfsmaccepts(edges, [5], 1, "abyc", []);
#
#def test(re_string, e, ac_s, st_s, strings):
#    my_e, my_ac_s, my_st_s = re_to_nfsm(re_string) 
#    print my_e
#    for string in strings:
#        print nfsmaccepts(e,ac_s,st_s,string,[]) == nfsmaccepts(my_e,my_ac_s,my_st_s,string,[]) 
#
#edges = { (1,'a')  : [ 2 ] ,
#          (2,None) : [ 3 ] ,    # epsilon transition
#          (2,'b')  : [ 2 ] ,
#          (3,'c')  : [ 4 ] } 
#accepting_state = [4]
#start_state = 1
#
#test("a(b*)c", edges, accepting_state, start_state, 
#  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 
#
#edges = { (1,'a')  : [ 2 ] ,
#          (2,'b') :  [ 1 ] ,    
#          (1,'c')  : [ 3 ] ,
#          (3,'d')  : [ 1 ] } 
#accepting_state = [1]
#start_state = 1
#
#test("((ab)|(cd))*", edges, accepting_state, start_state, 
#  [ "", "ab", "cd", "cddd", "c", "", "ad", "abcd", "abbbbbc", "ac" ]  ) 
