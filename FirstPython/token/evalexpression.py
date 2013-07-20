# Quiz: Eval Exp

# Write an eval_exp procedure to interpret JavaScript arithmetic expressions.
# Only handle +, - and numbers for now.

def eval_exp_simple(tree):
    # ("number" , "5")
    # ("binop" , ... , "+", ... )
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "binop":
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        # QUIZ: (1) evaluate left and right child
        # (2) perform "operator"'s work
        left_value = eval_exp_simple(left_child);
        right_value = eval_exp_simple(right_child);
        if operator == '+':
            return left_value + right_value;
        elif operator == '-':
            return left_value - right_value;

        

test_tree1 = ("binop",("number","5"),"+",("number","8"))
print eval_exp_simple(test_tree1) == 13

test_tree2 = ("number","1776")
print eval_exp_simple(test_tree2) == 1776

test_tree3 = ("binop",("number","5"),"+",("binop",("number","7"),"-",("number","18")))
print eval_exp_simple(test_tree3) == -6


# QUIZ : Variable Lookup

# Adding variable lookup to the interpreter!

def eval_exp_tree(tree, environment):
    nodetype = tree[0]
    if nodetype == "number":
        return int(tree[1])
    elif nodetype == "binop":
        left_value = eval_exp_tree(tree[1], environment)
        operator = tree[2]
        right_value = eval_exp_tree(tree[3], environment)
        if operator == "+":
            return left_value + right_value
        elif operator == "-":
            return left_value - right_value
    elif nodetype == "identifier":
        # ("binop", ("identifier","x"), "+", ("number","2"))
        # QUIZ: (1) find the identifier name
        # (2) look it up in the environment and return it
        variable_name = tree[1];
        if variable_name in environment:
            return env_lookup(environment, variable_name);


# Here's some code to simulate env_lookup for now. It's not quite what we'll be
# using by the end of the course.

def env_lookup(env,vname): 
    return env.get(vname,None)

environment = {"x" : 2}
tree = ("binop", ("identifier","x"), "+", ("number","2"))
print eval_exp_tree(tree,environment) == 4


# QUIZ: Evaluating Statements

def eval_stmts(tree, environment):
    stmttype = tree[0]
    if stmttype == "assign":
        # ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
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

        
def eval_exp(exp, env): 
    etype = exp[0] 
    if etype == "number":
        return float(exp[1])
    elif etype == "string":
        return exp[1] 
    elif etype == "true":
        return True
    elif etype == "false":
        return False
    elif etype == "not":
        return not(eval_exp(exp[1], env))

def env_update(env, vname, value):
    env[vname] = value
        
environment = {"x" : 2}
tree = ("if-then-else", ("true", "true"), ("assign", "x", ("number", "8")), ("assign", "x", "5"))
eval_stmts(tree, environment)
print environment;
print environment == {"x":8}

         
