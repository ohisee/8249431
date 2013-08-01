# "I Could Wile Away The Hours"
#
# 
# Although our HTML and JavaScript interpreters are not yet integrated into
# a single browser, we can still extend our JavaScript interpreter
# independently. We already have support for recursive functions and "if"
# statements, but it would be nice to add support for "while".
#
# Consider the following two JavaScript fragments:
#
#    var i = 0;
#    while (i <= 5) {
#      document.write(i); 
#      i = i + 2;
#    };
#
# And: 
#
#    function myloop(i) {
#      if (i <= 5) {
#         document.write(i);
#         myloop(i + 2);
#      } ;
#    }
#    myloop(0);
#
# They both have the same effect: they both write 0, 2 and 4 to the
# webpage. (In fact, while loops and recursion are equally powerful! You
# really only need one in your language, but it is very convenient to have
# them both.) 
#
# We can extend our lexer to recognize 'while' as a keyword. We can extend
# our parser with a new statement rule like this: 
#
#    def p_stmt_while(p):
#        'stmt : WHILE exp compoundstmt'
#         p[0] = ("while",p[2],p[3])
#
# Now we just need to extend our interpreter to handle while loops. The
# meaning of a while loop is: 
#
#       1. First, evaluate the conditional expression in the current
#       environment. If it evaluates to false, stop.
#
#       2. Evaluate the body statements in the current environment. 
#
#       3. Go to step 1. 
#
# Recall that our JavaScript interpreter might have functions like:
#
#       eval_stmts(stmts,env)
#       eval_stmt(stmt,env)
#       eval_exp(exp,env) 
#
# For this assignment, you should write a procedure:
#
#       eval_while(while_stmt,evn) 
#
# Your procedure can (and should!) call those other procedures. Here is 
# how our interpreter will call your new eval_while(): 
# 
# def eval_stmt(stmt,env): 
#         stype = stmt[0] 
#         if stype == "if-then":
#                 cexp = stmt[1]
#                 then_branch = stmt[2] 
#                 if eval_exp(cexp,env):
#                         eval_stmts(then_branch,env) 
#         elif stype == "while":
#                 eval_while(stmt,env) 
#         elif stype == "if-then-else":
#                 ...
#
# Hint 1: We have structured this problem so that it is difficult for you
# to test (e.g., because we have not provided you the entire JavaScript
# interpreter framework). Thus, you should think carefully about how to
# write the code correctly. Part of the puzzle of this exercise is to
# reason to the correct answer without "guess and check" testing.
#
# Hint 2: It is totally legal to define JavaScript's while using a Python
# while statement. (Remember, an interpreter is like a translator.) You
# could also define JavaScript's while using recursion in Python.
#
# Hint 3: Extract the conditional expression and while loop body statements
# from while_stmt first. 

def eval_stmt(tree, environment):
    stmttype = tree[0]
    if stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+", ...)) <=== x = ... + ...
        variable_name = tree[1]
        right_child = tree[2]
        new_value = eval_exp(right_child, environment)
        env_update(environment, variable_name, new_value)
    elif stmttype == "if-then-else": # if x < 5 then A;B; else C;D;
        conditional_exp = tree[1] # x < 5
        then_stmts = tree[2] # A;B;
        else_stmts = tree[3] # C;D;
        # QUIZ: Complete this code
        # Assume "eval_stmts(stmts, environment)" exists
        if eval_exp(conditional_exp, environment) == True:
            eval_stmts(then_stmts, environment);
        else:
            eval_stmts(else_stmts, environment);
    elif stmttype == "while":
        eval_while(tree, environment);
        
def eval_exp(exp, env):
    etype = exp[0]
    if etype == "number":
        return float(exp[1]);
    elif etype == "string":
        return exp[1]
    elif etype == "true":
        return True;
    elif etype == "false":
        return False;
    elif etype == "not":
        return not(eval_exp(exp[1], env));
    elif etype == "binop":
        left_value = eval_exp(exp[1], env)
        operator = exp[2]
        right_value = eval_exp(exp[3], env)
        if operator == "+":
            return left_value + right_value;
        elif operator == "-":
            return left_value - right_value;
        elif operator == "*":
            return left_value * right_value;
        elif operator == "/":
            return left_value / right_value;
        elif operator == "%":
            return left_value % right_value;
        elif operator == "==":
            return left_value == right_value;
        elif operator == "<=":
            return left_value <= right_value;
        elif operator == "<":
            return left_value < right_value;
        elif operator == ">=":
            return left_value >= right_value;
        elif operator == ">":
            return left_value > right_value;
        elif operator == "&&":
            return left_value and right_value;
        elif operator == "||":
            return left_value or right_value;
    elif etype == "identifier":
        # ("binop", ("identifier","x"), "+", ("number","2"))
        # QUIZ: (1) find the identifier name
        # (2) look it up in the environment and return it
        variable_name = exp[1];
        if variable_name in env:
            return env_lookup(env, variable_name);

def env_update(env, vname, value):
    env[vname] = value;
    
def env_lookup(env, vname):
    return env.get(vname, None);

def eval_stmts(stmts, env): 
    for stmt in stmts:
        eval_stmt(stmt, env);

def eval_while(while_stmt, env):
    # Fill in your own code here. Can be done in as few as 4 lines.
    conditional_exp = while_stmt[1];
    while_stmt_body = while_stmt[2];
    while eval_exp(conditional_exp, env):
        eval_stmts(while_stmt_body, env);

environment = {"i" : 0}
w = ('while', ('binop', ('identifier', 'i'), '<=', ('number', 5.0)), [('assign', 'i', ('binop', ('identifier', 'i'), '+', ('number', 2.0)))])
eval_stmt(w, environment);
print (environment);
