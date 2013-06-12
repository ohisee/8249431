# Valid Statements

# Translate the following JavaScript code to Python:

#        function mymin(a, b){
#            if (a < b){
#                return a;
#            } else {
#                return b;
#            };
#        }
#        
#        function square(x){
#            return x * x;
#        }
#        
#        write(mymin(square(-2), square(3)));

def mymin(a, b):
    if a < b:
        return a;
    else:
        return b;
    
def square(x):
    return x * x;

print (mymin(square(-2), square(3)));


# Small Words

# Write a Python generator function called small_words 
# that accepts a list of strings as input and yields 
# those that are at most 3 letters long.

def small_words(words):
    for word in words:
        if len(word) <= 3:
            yield word;
            
# Expanding Exp
# This is very, very difficult.

grammar = [ 
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ]


def expand(tokens, grammar):
    for pos in range(len(tokens)):
        #print ("Pos '%s'" % tokens[pos]);
        for rule in grammar:
            #print rule[0];
            if tokens[pos] == rule[0]:
                r = tokens[0:pos] + rule[1] + tokens[pos+1:];
                yield r;
#             else:
#                 yield tokens;
#             if rule[0] == tokens[pos]:
#                 yield rule[1];    
#expand(['a', 'exp'], grammar);       
            
depth = 1
utterances = [["a", "exp"]]
for x in range(depth):
    for sentence in utterances:
        utterances = utterances + [ i for i in expand(sentence, grammar)]

#print utterances;
for sentence in utterances:
    print sentence
    
#    ['exp']
#    ['exp', '+', 'exp']
#    ['exp', '-', 'exp']
#    ['(', 'exp', ')']
#    ['num']


# Bonus Practice: Subsets

# This assignment is not graded and we encourage you to experiment. Learning is
# fun!

# Write a procedure that accepts a list as an argument. The procedure should
# print out all of the subsets of that list.
lst = ['a', 'b', 'c'];
def get_sub_list(remaining, showed):
    #print ('remaining %s' % remaining);
    #print ('showed %s' % showed);
    
    if not remaining:
        #print ('no more remaining');
        if showed is not None:
            print (showed);
        return showed;
    else:
        showed.append(remaining[0]);
        #print ('calling invite 1');
        get_sub_list(remaining[1:], showed);
        #print ('invite 1 result:')
        #print ('-------------------------------------- %s' % r);
        #print ('calling invite 2');
        showed.pop();
        get_sub_list(remaining[1:], showed);
        #print ('invite 2 result');
        #print ('-------------------------------------- %s' % r);

def gen_sub_list(remaining, showed):
    if not remaining:
        return [showed];
    else:
        ns = [] + showed;
        ns.append(remaining[0]);
        return gen_sub_list(remaining[1:], ns) + gen_sub_list(remaining[1:], showed);
        
        
def sub_list(lst):
    get_sub_list(lst, []);

#print ('hello');
#sub_list(lst);
#print ('hello again')
#print (gen_sub_list(lst, []));

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

def cfgempty(grammar,symbol,visited):
    
    print ('Symbol %s' % symbol);
    for g in grammar:
        if symbol != g[0] and symbol in g[1]:
            return [];
        
    if symbol in visited:
        return None;
    else:
        for rw_rule in grammar:
            if rw_rule[0] == symbol and any(rw_rule[1]):
                for rw in rw_rule[1]:
                    print ('Visiting %s' % rw);
                    visited.append(rw);
                    r = cfgempty(grammar, rw, visited);
                    if r is not None:
                        return r.append(rw);
        return None;
                    
# We have provided a few test cases for you. You will likely want to add
# more of your own. 

#grammar1 = [ 
#      ("S", [ "P", "a" ] ),           
#      ("P", [ "S" ]) ,               
#      ] 
#                        
#print cfgempty(grammar1,"S",[]) == None 

grammar2 = [
      ("S", ["P", "a" ]),             
      ("S", ["Q", "b" ]),             
      ("P", ["P"]), 
      ("Q", ["c", "d"]),              
      ] 

print (cfgempty(grammar2,"S",[]));
print cfgempty(grammar2,"S",[]) == ['c', 'd', 'b']


#grammar3 = [  # some Spanish provinces
#        ("S", [ "Barcelona", "P", "Huelva"]),
#        ("S", [ "Q" ]),
#        ("Q", [ "S" ]),
#        ("P", [ "Las Palmas", "R", "Madrid"]),
#        ("P", [ "T" ]),
#        ("T", [ "T", "Toledo" ]),
#        ("R", [ ]) ,
#        ("R", [ "R"]), 
#        ]
#
#print cfgempty(grammar3,"S",[]) == ['Barcelona', 'Las Palmas', 'Madrid', 'Huelva']

        