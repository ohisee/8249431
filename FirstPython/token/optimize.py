# Bending Numbers
#
# In class we discussed a number of arithmetic optimizations for
# JavaScript. In our approach to optimization, a sub-tree of the
# abstract syntax is replaced with a new abstract syntax tree. 
#
# In addition to using arithmetic identities, such as X*0 == 0 for all X,
# we can also perform arithmetic operations on constants. For example, if 
# a JavaScript loop or recursive procedure containts 1+2+3, we can just
# evaluate it to 6 once and then not perform the two additions again.
# This technique is called "constant folding". 
#
# Write a procedure optimize(exp) that takes a JavaScript expression AST
# node and returns a new, simplified JavaScript expression AST. You must
# handle:
#
#       X * 1 == 1 * X == X     for all X
#       X * 0 == 0 * X == 0     for all X
#       X + 0 == 0 + X == X     for all X
#       X - X == 0              for all X
#
#       and constant folding for +, - and * (e.g., replace 1+2 with 3) 
#
# To do constant folding, given a parse tree for X+Y we want to try to add
# the values for the parse trees of X and Y. If X and Y are both numbers,
# that will work. But if X or Y is an identifier, for example, that will
# not work, because the types will not match. 

def optimize(exp): 
    etype = exp[0] 
    if etype == "binop":
        a = optimize(exp[1])
        op = exp[2]
        b = optimize(exp[3])

        # Try Arithmetic Laws
        if op == "*" and (a == ("number",0) or b == ("number",0)):
            return ("number",0) 
        # Fill in more optimizations here ...
        elif (op == "-") and (a == b):
            return ("number", 0);
        elif op == "*" and b == ("number", 1):
            return a;
        elif op == "*" and a == ("number", 1):
            return b;
        elif op == "*" and b == ("number", 0):
            return b;
        elif op == "*" and a == ("number", 0):
            return a;
        elif op == "+" and b == ("number", 0):
            return a;
        elif op == "+" and a == ("number", 0):
            return b;
        # Try Constant Folding
        # Fill in more optimizations here ...
        elif (a[0] == "number") and (b[0] == "number"):
            l_val = a[1];
            r_val = b[1];
            if op == "+":
                return ("number", l_val + r_val);
            elif op == "-":
                return ("number", l_val - r_val);
            elif op == "*":
                return ("number", l_val * r_val);
            #elif op == "/":
                #return ("number", l_val / r_val);
        
        # If all else fails, return something good here ...
        return (etype, a, op, b);

    # leave this expression un-optimized 
    return exp

# We have prepared some test cases. You may want to try your own.
zero            = ("number", 0.0) 
one             = ("number", 1.0) 
two             = ("number", 2.0) 
xerxes          = ("var","xerxes") # Kings and Queens of Persia and Macedonia
darius          = ("var","darius") 
antiochus       = ("var","antiochus") 
musa            = ("var","musa")   
def plus(a,b):
    return ("binop",a,"+",b) 
def minus(a,b):
    return ("binop",a,"-",b) 
def times(a,b):
    return ("binop",a,"*",b) 

exp6 = minus(musa, musa);
print optimize(exp6);

exp1 = times(two,zero) 
print optimize(exp1) == zero 

exp2 = times(darius,minus(two,two))
print optimize(exp2);
print optimize(exp2) == zero 

exp3 = minus(plus(zero,plus(one,plus(two,zero))),two)
print optimize(exp3) == one

five = plus(two,plus(two,one))
exp4 = times(five,(plus(minus(musa,musa),plus(musa,zero))))
print optimize(exp4);
print optimize(exp4) == ('binop', ('number', 5.0), '*', ('var', 'musa'))

big_exp = zero 
for i in range(10):
    big_exp = ("binop",big_exp,"+",("number",i))
print optimize(big_exp) == ("number", 45.0) # 0+1+2+3+4+5+6+7+8+9

exp7 = ('binop', ('binop', ('var', 'musa'), '-', ('var', 'musa')), '+', ('binop', ('var', 'musa'), '+', ('number', 0.0)));
print (optimize(exp7));


# The Living and the Dead
#
# In addition to optimizing expressions, it is also possible to optimize
# statements. There are many ways to do so, and we will explore one in this
# problem. 
#
# (This problem description looks long, but that is mostly because it
# contains a few worked examples.) 
#
# Consider this JavaScript fragment: 
#
#       function myfun(a,b,c,d) {
#               a = 1;
#               b = 2;
#               c = 3;
#               d = 4; 
#               a = 5;
#               d = c + b;
#               return (a + d);
#       } 
#
# Many of the assignment statements end up computing values that are never
# used. The output of the function only really depends on the final values
# of a and d. This function, with two of the lines removed, computes the
# same answer: 
#
#       function myfun(a,b,c,d) {
#               # a = 1;
#               b = 2;
#               c = 3;
#               # d = 4; 
#               a = 5;
#               d = c + b;
#               return (a + d);
#       } 
#
# Those lines can be safely removed because they do not compute a value
# that is used later. We say that a variable is LIVE if the value it holds
# may be needed in the future. More formally, a variable is LIVE if its
# value may be read before the next time it is overwritten. Whether or not
# a variable is LIVE depends on where you are looking in the program, so
# most formally we say a variable is live at some point P if it may be read
# before being overwritten after P. 
#
# We can compute the set of live variables by looking at the statements in
# the function in reverse order. 
#
#               return (a + d);
#
# Since the output of the function depends on (a + d), a and d are both
# live right before this statement. Now we consider one more statement: 
#
#               d = c + b;
#               return (a + d);
# 
# "a" and "d" were live going in to the return statement. What is live
# before "d = c + b"? Well, since "d" is overwritten, we have to remove it
# from the set. But since "c" and "b" are written, we have to add them to
# the set. So the set of live variables before that assignment statement is
# "a", "b", "c". In fact, we could annotate the whole program: 
#
#       function myfun(a,b,c,d) {
#               a = 1;
#               # LIVE: nothing 
#               b = 2;
#               # LIVE: b 
#               c = 3;
#               # LIVE: c, b
#               d = 4; 
#               # LIVE: c, b 
#               a = 5;
#               # LIVE: a, c, b 
#               d = c + b;
#               # LIVE: a, d
#               return (a + d);
#       } 
#
# Once we know which variables are LIVE, we can now remove assignments to
# variables that will never be read later. Such assignments are called DEAD
# code. Formally, given an assignment statement "X = ...", if "X" is not
# live after that statement, the whole statement can be removed. 
#
# Note that remove some dead code may make it possible to remove more
# later. For example, in this fragment:
#
#               a = 1;
#               b = a + 1;
#               c = 2;
#               return c; 
#
# We can initially find the following LIVE variables: 
#
#               a = 1;
#               # LIVE: a
#               b = a + 1;
#               # LIVE: nothing
#               c = 2;
#               # LIVE: c
#               return c; 
#
# But if we remove the "b = a + 1" assignment and repeat the process, we
# will be able to remove the "a = 1" code as well!
#
# In this assignment, you will write an optimizer that removes dead code. 
# For simplicity, we will only consider sequences of assignment statements
# (once we can optimize those, we could weave together a bigger optimizer
# that handles both branches of if statements, and so on, but we'll just do
# simple lists of assignments for now). 
#
# We will encode JavaScript fragments as lists of tuples. For example,
#
#               a = 1;
#               b = a + 1;
#               c = 2;
#
# Will be encoded as:
#
fragment2 = [ ("a", ["1"] ) ,           # a = 1
              ("b", ["a", "1"] ),       # b = a operation 1
              ("c", ["2"] ), ]          # c = 2 
# 
# That is, each assignment "LHS = RHS op RHS op RHS ..." will just be
# encoded as (LHS, [RHS, RHS, RHS]). A block is then a list of such
# assignments. 
#
# Write a procedure removedead(fragment,returned). "fragment" is encoded
# as above. "returned" is a list of variables returned at the end of the
# fragment (and thus LIVE at the end of it). 
#
# Hint 1: One way to reverse a list is [::-1] 
# >>> [1,2,3][::-1]
# [3, 2, 1]
#
# Hint 2: One "functional programming" way to make a new list that is just
# like L but with all copies of X removed is:
# [ e for e in L if e != X ] 
#
# Hint 3: Remember that if anything changes, you should call yourself
# recursively because you may find even more dead code!  

#       function myfun(a,b,c,d) {
#               a = 1;
#               # LIVE: nothing 
#               b = 2;
#               # LIVE: b 
#               c = 3;
#               # LIVE: c, b
#               d = 4; 
#               # LIVE: c, b 
#               a = 5;
#               # LIVE: a, c, b 
#               d = c + b;
#               # LIVE: a, d
#               return (a + d);
#       } 

def removedead(fragment,returned):
    # fill in your answer here (can be done in about a dozen lines)
    live, live_fragment = returned, [];
    for elt in fragment[::-1]:
        if elt[0] in live:
            live_fragment.append(elt);
            live.pop(live.index(elt[0]));
            live += [rhs for rhs in elt[1] if rhs in [lhs[0] for lhs in fragment]];
    return live_fragment[::-1];
        

# We have provided a few test cases. You may want to write your own.

fragment1 = [ ("a", ["1"]), 
              ("b", ["2"]), 
              ("c", ["3"]), 
              ("d", ["4"]), 
              ("a", ["5"]), 
              ("d", ["c","b"]), ]


removedead (fragment1, ["a","d"]);
removedead (fragment2, ["c"]);

print removedead(fragment1, ["a","d"]) == [('b', ['2']), ('c', ['3']), ('a', ['5']), ('d', ['c', 'b'])]
print removedead(fragment2, ["c"]) == [('c', ['2'])]
print removedead(fragment1, ["a"]) == [('a', ['5'])]
print removedead(fragment1, ["d"]) == [('b', ['2']), ('c', ['3']), ('d', ['c', 'b'])]

