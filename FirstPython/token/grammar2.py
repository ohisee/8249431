# Reading Machine Minds 2
#
# We say that a finite state machine is "empty" if it accepts no strings.
# Similarly, we say that a context-free grammar is "empty" if it accepts no
# strings. In this problem, you will write a Python procedure to determine
# if a context-free grammar is empty.
#
# A context-free grammar is "empty" starting from a non-terminal symbol S 
# if there is no _finite_ sequence of rewrites starting from S that
# yield a sequence of terminals. 
#
# For example, the following grammar is empty:
#
# grammar1 = [ 
#       ("S", [ "P", "a" ] ),           # S -> P a
#       ("P", [ "S" ]) ,                # P -> S
#       ] 
#       
# Because although you can write S -> P a -> S a -> P a a -> ... that
# process never stops: there are no finite strings in the language of that
# grammar. 
#
# By contrast, this grammar is not empty: 
#
# grammar2 = [
#       ("S", ["P", "a" ]),             # S -> P a
#       ("S", ["Q", "b" ]),             # S -> Q b
#       ("P", ["P"]),                   # P -> P
#       ("Q", ["c", "d"]),              # Q -> c d 
#
# And ["c","d","b"] is a witness that demonstrates that it accepts a
# string.
#
# Write a procedure cfgempty(grammar,symbol,visited) that takes as input a
# grammar (encoded in Python) and a start symbol (a string). If the grammar
# is empty, it must return None (not the string "None", the value None). If
# the grammar is not empty, it must return a list of terminals
# corresponding to a string in the language of the grammar. (There may be
# many such strings: you can return any one you like.) 
#
# To avoid infinite loops, you should use the argument 'visited' (a list)
# to keep track of non-terminals you have already explored. 
#
# Hint 1: Conceptually, in grammar2 above, starting at S is not-empty with
# witness [X,"a"] if P is non-empty with witness X and is non-empty with
# witness [Y,"b"] if Q is non-empty with witness Y. 
#
# Hint 2: Recursion! A reasonable base case is that if your current
# symbol is a terminal (i.e., has no rewrite rules in the grammar), then
# it is non-empty with itself as a witness. 
#
# Hint 3: all([True,False,True]) = False
#         any([True,True,False]) = True
    
def is_terminal(grammar,symbol):
    return not any([g[0] == symbol for g in grammar]) and any([symbol in g[1] for g in grammar]);
    
def cfgempty_check(grammar,symbol,visited):
    if symbol in visited:
        return None;
    else:
        result = [];
        visited.append(symbol);
        for pos in range(len(grammar)):
            if grammar[pos][0] == symbol:
                local = [];
                for rule in grammar[pos][1]:
                    if is_terminal(grammar, rule):
                        local = local + [rule];
                    else:
                        r = cfgempty_check(grammar, rule, visited);
                        if r is not None and all(r):
                            local = local + r;
                        else:
                            del local[:];
                            local.append(False);
                            break;
                result = result + local;
                
                if all(result):
                    break;
            
        return result;
        
def cfgempty(grammar,symbol,visited):
    result = cfgempty_check(grammar,symbol,visited);
    if result:
        if result[0] == False:
            return result[1:] if result[1:] else None;
        return result;
    return result;
         
# We have provided a few test cases for you. You will likely want to add
# more of your own. 

grammar1 = [ 
      ("S", [ "P", "a" ] ),           
      ("P", [ "S" ]) ,               
      ] 

grammar21 = [ 
      ("S", [ ] ),           
      ("S", [ "S" ]) ,               
      ] 

#print (cfgempty(grammar21,"S",[]));             
#print cfgempty(grammar1,"S",[]) == None 

grammar2 = [
      ("S", ["P", "a" ]),             
      ("S", ["Q", "b" ]),             
      ("P", ["P"]), 
      ("Q", ["c", "d"]),              
      ] 

grammar12 = [
      ("S", ["a", "P", "b" ]),             
      ("P", []),
      ("S", ["c"]),
      ] 

grammar13 = [
      ("S", ["P", "a"]),             
      ("P", ["Q"]),
      ("Q", ["M"]),
      ("M", ["b", "c"]),
      ] 

#print (cfgempty(grammar13,"S",[]));
#print cfgempty(grammar2,"S",[]) == ['c', 'd', 'b']


grammar3 = [  # some Spanish provinces
        ("S", [ "Barcelona", "P", "Huelva"]),
        ("S", [ "Q" ]),
        ("Q", [ "S" ]),
        ("P", [ "Las Palmas", "R", "Madrid"]),
        ("P", [ "T" ]),
        ("T", [ "T", "Toledo" ]),
        ("R", [ ]) ,
        ("R", [ "R"]), 
        ]

#print (cfgempty(grammar3,"S",[]));
#print cfgempty(grammar3,"S",[]) == ['Barcelona', 'Las Palmas', 'Madrid', 'Huelva']


grammar123 = [
              ('S', ['Barcelona', 'P', 'Huelva']), 
              ('S', ['Q']), 
              ('Q', ['S']), 
              ('P', ['Las Palmas', 'R', 'Madrid']), 
              ('P', ['T']), 
              ('T', ['T', 'Toledo']), 
              ('R', []), 
              ('R', ['R']),
              ]

#print (cfgempty(grammar123,"R",[]));

def cfgempty_s(grammar, symbol, visited): 
    if symbol in visited: # no infinite loops! 
        return None 
    elif not any([ rule[0] == symbol for rule in grammar ]): 
        # base case: 'symbol' is a terminal 
        return [symbol] 
    else: 
        new_visited = visited + [symbol] 
        # consider every rewrite rule "Symbol -> RHS" 
        for rhs in [r[1] for r in grammar if r[0] == symbol]: # check if every part of RHS is non-empty 
            if all([None != cfgempty_s(grammar, r, new_visited) for r in rhs]): 
                result = [] # gather up the result 
                for r in rhs: 
                    result = result + cfgempty_s(grammar, r, new_visited) 
                return result # didn't find any return None 
    
# Infinite Mind Reading
#
# Just as a context-free grammar may be 'empty', it may also have an
# infinite language. We say that the language for a grammar is infinite if
# the grammar accepts an infinite number of different strings (each of
# which is of finite length). Most interesting (and creative!) languages
# are infinite.
# 
# For example, the language of this grammar is infinite:
#
# grammar1 = [ 
#       ("S", [ "S", "a" ] ),        # S -> S a
#       ("S", [ "b", ]) ,            # S -> b 
#       ] 
#
# Because it accepts the strings b, ba, baa, baaa, baaaa, etc. 
#
# However, this similar grammar does _not_ have an infinite language: 
#
# grammar2 = [ 
#       ("S", [ "S", ]),             # S -> S 
#       ("S", [ "b", ]) ,            # S -> b 
#       ] 
#
# Because it only accepts one string: b. 
#
# For this problem you will write a procedure cfginfinite(grammar)
# that returns True (the value True, not the string "True") if the grammar
# accepts an infinite number of strings (starting from any symbol). Your
# procedure should return False otherwise. 
#
# Consider this example: 
# 
# grammar3 = [ 
#       ("S", [ "Q", ] ),        # S -> Q
#       ("Q", [ "b", ]) ,        # Q -> b
#       ("Q", [ "R", "a" ]),     # Q -> R a 
#       ("R", [ "Q"]),           # R -> Q
#       ] 
#
# The language of this grammar is infinite (b, ba, baa, etc.) because it is
# possible to "loop" or "travel" from Q back to Q, picking up an "a" each
# time. Since we can travel around the loop as often as we like, we can
# generate infinite strings. By contrast, in grammar2 it is possible to
# travel from S to S, but we do not pick up any symbols by doing so. 
#
# Important Assumption: For this problem, you may assume that for every
# non-terminal in the grammar, that non-terminal derives at least one
# non-empty finite string.  (You could just call cfgempty() from before to
# determine this, so we'll assume it.)  
#
# Hint 1: Determine if "Q" can be re-written to "x Q y", where either x
# or y is non-empty. 
#
# Hint 2: The "Important Assumption" above is more important than it looks:
# it means that any rewrite rule "bigger" than ("P", ["Q"]) adds at least
# one token. 
#
# Hint 3: While cfginfinite(grammar) is not recursive, you may want to
# write a helper procedure (that determines if Q can be re-written to "x Q
# y" with |x+y| > 0 ) that _is_ recursive. Watch out for infinite loops:
# keep track of what you have already visited. 

def only_terminal(sym_lst, grammar):
    for sym in sym_lst:
        if any([g[0] == sym for g in grammar]):
            return False;
    return True;

def rewrite_cfg_symbol(symbol, grammar, visited):
    # Terminal
    if not any([g[0] == symbol for g in grammar]) and any([symbol in g[1] for g in grammar]):
        return [symbol];
    elif symbol in visited:
        return None;
    else:
        uv = visited + [symbol];
        #print ("Symbol is %s" % symbol);
        for rhs in [rule[1] for rule in grammar if rule[0] == symbol and not only_terminal(rule[1], grammar)]:
            result = [];
            for rw_sym in rhs:
                r = rewrite_cfg_symbol(rw_sym, grammar, uv);
                if r is not None:
                    result = result + r;
                else:
                    result = result + [rw_sym];
                #print ("Result is %s" % result);
            return result;
                
        
    
def cfginfinite(grammar): 
    for q in [rule[0] for rule in grammar]:
        result = rewrite_cfg_symbol(q, grammar, []);
        if result and q in result and len(result) > 1:
            return True;
    return False;

# We have provided a few test cases. You will likely want to write your own
# as well. 

grammar1 = [ 
      ("S", [ "S", "a" ]), # S -> S a
      ("S", [ "b", ]) , # S -> b 
      ] 
print cfginfinite(grammar1) == True

grammar2 = [ 
      ("S", [ "S", ]), # S -> S 
      ("S", [ "b", ]) , # S -> b 
      ] 

print cfginfinite(grammar2) == False

grammar3 = [ 
      ("S", [ "Q", ]), # S -> Q
      ("Q", [ "b", ]) , # Q -> b
      ("Q", [ "R", "a" ]), # Q -> R a 
      ("R", [ "Q"]), # R -> Q
      ] 

print cfginfinite(grammar3) == True

grammar4 = [  # Nobel Peace Prizes, 1990-1993
      ("S", [ "Q", ]),
      ("Q", [ "Mikhail Gorbachev", ]) ,
      ("Q", [ "P", "Aung San Suu Kyi" ]),
      ("R", [ "Q"]),
      ("R", [ "Rigoberta Tum"]),
      ("P", [ "Mandela and de Klerk"]),
      ] 

print cfginfinite(grammar4) == False

grammar12 = [ 
       ("S", [ "Q", ] ),        # S -> Q
       ("Q", [ "b", ]) ,        # Q -> b
       ("Q", [ "a", "R", ]),     # Q -> R a 
       ("R", [ "S"]),           # R -> Q
       ] 

grammar122 = [ 
       ("S", [ "P", "a" ] ),           # S -> P a
       ("P", [ "Q" ]) ,                # P -> S
       ("Q", [ "R" ]),
       ("R", [ "S", "b" ]),
       ("O", [ "Z" ]),
       ] 

print (rewrite_cfg_symbol("Q", grammar12, []));
#mmm = [rule[1] for rule in grammar1 if rule[0] == 'S' and not only_terminal(rule[1], grammar1)];
#print (mmm);