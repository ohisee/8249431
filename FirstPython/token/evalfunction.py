# QUIZ : Frames
# Return will throw an excception
# Function Calls: new environments, catch return values

#
# Python Exception creates Exception (___someting___). 
# Must use except Exception as returnVal -> return returnVal[0] to get that ___something___.
# Followed the solution provided, use Python class to capture and get the return value.
#
class JavaScriptReturnVal(Exception):
    def __init__(self, ret_val):
        self.ret_val = ret_val;

def eval_stmt(tree, environment):
    print "calling eval_stmt";
    stmttype = tree[0];
    if stmttype == "assign":
        print (stmttype);
        # ("assign", "x", ("binop", ..., "+", ...)) <=== x = ... + ...
        variable_name = tree[1];
        right_child = tree[2];
        new_value = eval_exp(right_child, environment);
        print "assign stmt ", tree;
        print "assign new_value %f to variable %s" % (new_value, variable_name);
        env_update(variable_name, new_value, environment);
    elif stmttype == "if-then-else": # if x < 5 then A;B; else C;D;
        print (stmttype);
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
        print (stmttype);
        eval_while(tree, environment);
    elif stmttype == "return": 
        print (stmttype);
        retval = eval_exp(tree[1], environment);
        #raise Exception(retval);
        raise JavaScriptReturnVal(retval);
    elif stmttype == "exp":
        print (stmttype); 
        eval_exp(tree[1], environment);
    elif stmttype == "var": 
        variable_name = tree[1];
        print "     environment of variable [%s] " % variable_name;
        rhs = tree[2];
        (environment[1])[variable_name] = eval_exp(rhs, environment);
        print "     environment of variable [%s] : " % variable_name, environment[1];
            
def env_lookup(vname, env): 
    if vname in env[1]:
        return (env[1])[vname];
    elif env[0] == None:
        return None;
    else:
        return env_lookup(vname, env[0]);

def env_update(vname, value, env):
    if vname in env[1]:
        (env[1])[vname] = value;
    elif not (env[0] == None):
        env_update(vname,value,env[0]);
                
                
def eval_exp(exp, env): 
    etype = exp[0];
    print "eval expression is %s " % etype;   
    if etype == "number":
        print "eval expression -> return number %s " % exp[1];
        return float(exp[1]);
    elif etype == "string":
        return str(exp[1]);
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
        vname = exp[1]
        print "eval expression -> identifier %s" % vname;
        value = env_lookup(vname, env);
        print "eval expression -> identifier %s with value" % vname, value; 
        if value == None: 
            print "ERROR: unbound variable " + vname
        else:
            return value;
    elif etype == "function":  # ("function", ["x", "y"], [ ("return", ("binop", ...) ])
        fparams = exp[1];
        fbody = exp[2];
        return ("function", fparams, fbody, env);
    elif etype == "call": # ("call", "sqrt", [("number","2")])
        fname = exp[1] # "sqrt"
        args = exp[2] # [ ("number", "2") ]
        fvalue = env_lookup(fname, env); # None for write
        print "eval call function name : %s" % fname;
        # document.write() function
        if fname == "write":
            print "call -> write";
            for arg in args:
                argval = eval_exp(arg, env);
                output_sofar = env_lookup("javascript output", env);
                env_update("javascript output", output_sofar + str(argval), env);
            #return None;
        elif fvalue[0] == "function":
            # We'll make a promise to ourselves:
            # ("function", params, body, env)
            fparams = fvalue[1]; # ["x"]
            fbody = fvalue[2];
            fenv = fvalue[3]; # Get environment from 4th parameter -> function's env.
            print "eval call -> function : %s | params " % fname, fparams, " | ", fbody;
            if len(fparams) <> len(args):
                print "ERROR: wrong number of args"
            else:
                #QUIZ: Make a new environment frame
                new_env = (fenv, {}); 
                for i in range(len(args)):
                    value = eval_exp(args[i], env);
                    (new_env[1])[fparams[i]] = value;
                    print "eval call function : %s | receive return value %s | new env " % (fname, value), new_env[1];
                try:
                    # QUIZ : Evaluate the body
                    eval_stmts(fbody, new_env);
                    return None
                except JavaScriptReturnVal as jsReturnVal:
                    return jsReturnVal.ret_val;
        else:
            print  "ERROR: call to non-function %s" % fname;

def eval_stmts(stmts, env): 
    for stmt in stmts:
        eval_stmt(stmt, env);

def eval_while(while_stmt, env):
    # Fill in your own code here. Can be done in as few as 4 lines.
    conditional_exp = while_stmt[1];
    while_stmt_body = while_stmt[2];
    while eval_exp(conditional_exp, env):
        eval_stmts(while_stmt_body, env);

#
# Optimize tree
#       
def optimize(tree):
    etype = tree[0];
    if etype == "binop":
        a = optimize(tree[1]);
        op = tree[2];
        b = optimize(tree[3]);
        if op == "*" and b == ("number", "1"):
            return a;
        elif op == "*" and b == ("number", "0"):
            return b;
        elif op == "+" and b == ("number", "0"):
            return a;
        return tree; #return changed
    return tree;

def eval_elt(elt, env):
    if elt[0] == 'function':
        fname = elt[1];
        fparams = elt[2];
        fbody = elt[3];
        fvalue = ("function",fparams,fbody,env);
        (env[1])[fname] = fvalue;        
    elif elt[0] == 'stmt':
        eval_stmt(elt[1], env);
    else:
        print "ERROR: eval_elt: unknown element " + elt;
        
def interpret(ast):
    global_environment = (None, {"javascript output" : ""});
    for element in ast:
        print "element is ------- : ", element;
        eval_elt(element, global_environment);
        for env_key in global_environment[1]:
            print "Global Env : [%s] " % env_key,
            print (global_environment[1])[env_key];        
    return (global_environment[1])["javascript output"];


#sqrt = ("function",("x"),(("return",("binop",("identifier","x"),"*",("identifier","x"))),),{})
#environment = (None, {"sqrt" : sqrt, "javascript output" : "", "tvtropes" : 3, "extracredits" : 4});

#print eval_exp(("call","sqrt",[("number","9")]),environment);
#print eval_exp(("call","write",[("string","abc"), ("string", " bbb")]),environment);
#print eval_exp(('function', ['x', 'y'], [('return', ('binop', ('number', 3.0), '+', ('number', 4.0)))]), environment);
#print (environment); 
#print optimize(("binop",("number","5"),"*",("number","1"))) == ("number","5");
#print optimize(("binop",("number","5"),"*",("number","0"))) == ("number","0");
#print optimize(("binop",("number","5"),"+",("number","0"))) == ("number","5");
#print optimize(("binop",("number","5"),"+",("binop",("number","5"),"*",("number","0"))))

#jsf = [('function', 'tvtropes', ['tgwtg'], [('var', 'theonion', ('binop', ('string', 'reddit'), '+', ('string', 'pennyarcade'))), ('var', 'loadingreadyrun', ('function', ['extracredits'], [('exp', ('call', 'write', [('identifier', 'tgwtg')])), ('exp', ('call', 'write', [('string', ' ')])), ('exp', ('call', 'write', [('identifier', 'theonion')])), ('exp', ('call', 'write', [('string', ' ')])), ('exp', ('call', 'write', [('identifier', 'extracredits')]))])), ('return', ('identifier', 'loadingreadyrun'))]), ('stmt', ('var', 'yudkowsky', ('call', 'tvtropes', [('number', 3.0)]))), ('stmt', ('var', 'tgwtg', ('number', 888.0))), ('stmt', ('var', 'extracredits', ('number', 999.0))), ('stmt', ('exp', ('call', 'yudkowsky', [('number', 4.0)])))];

jsf = [('stmt', ('var', 'a', ('number', 1.0))), ('stmt', ('var', 'x', ('number', 2.0))), ('stmt', ('var', 'y', ('number', 2.0))), ('function', 'myfun', ['x'], [('var', 'a', ('number', 3.0)), ('assign', 'x', ('binop', ('identifier', 'x'), '+', ('identifier', 'y'))), ('assign', 'y', ('binop', ('identifier', 'x'), '+', ('identifier', 'y'))), ('var', 'p', ('function', ['y', 'z'], [('var', 'q', ('function', ['x', 'z'], [('return', ('binop', ('identifier', 'x'), '+', ('binop', ('binop', ('identifier', 'a'), '*', ('identifier', 'y')), '/', ('identifier', 'z'))))])), ('return', ('identifier', 'q'))])), ('while', ('binop', ('binop', ('identifier', 'x'), '<', ('identifier', 'y')), '&&', ('binop', ('identifier', 'x'), '<', ('number', 10.0))), [('if-then-else', ('not', ('binop', ('identifier', 'x'), '<', ('identifier', 'y'))), [('assign', 'x', ('binop', ('identifier', 'x'), '-', ('number', 1.0)))], [('assign', 'x', ('binop', ('identifier', 'x'), '+', ('number', 1.0)))]), ('assign', 'a', ('binop', ('identifier', 'a'), '+', ('number', 1.0)))]), ('return', ('call', 'p', [('identifier', 'a'), ('identifier', 'y')]))]), ('stmt', ('var', 'f', ('call', 'myfun', [('identifier', 'y')]))), ('stmt', ('exp', ('call', 'write', [('call', 'f', [('number', 6.0), ('number', 7.0)])])))]

#jsf = [('function', 'foo', ['ax'], [('var', 'inside', ('function', ['ax'], [('exp', ('call', 'write', [('identifier', 'ax')]))])), ('return', ('identifier', 'inside'))]), ('stmt', ('var', 'ya', ('call', 'foo', [('number', 3.0)]))), ('stmt', ('exp', ('call', 'ya', [('number', 9.0)])))]

#jsf = [('function', 'foo', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))]), ('stmt', ('var', 'i', ('call', 'foo', [('number', 4.0)])))]

#jsf = [('function', 'foo', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))]), ('stmt', ('var', 'i', ('call', 'foo', [('number', 4.0)]))), ('stmt', ('exp', ('call', 'i', [('number', 4.0)])))]

#jsf = [('function', 'foo', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))]), ('stmt', ('var', 'i', ('call', 'foo', [('number', 4.0)]))), ('stmt', ('exp', ('call', 'write', [('call', 'i', [('number', 4.0)])])))]

print (interpret(jsf));

"""
  env[i] =  ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {'i': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {...}), {'ax': 4.0, 'pf': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {...}), {...}))})), 'javascript output': '', 'foo': ('function', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))], (None, {...}))}), {'ax': 4.0, 'pf': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {'i': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {...}), {...})), 'javascript output': '', 'foo': ('function', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))], (None, {...}))}), {...}))}))
  env[javascript output] =  
  env[foo] =  ('function', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))], (None, {'i': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {...}), {'ax': 4.0, 'pf': ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))], ((None, {...}), {...}))})), 'javascript output': '', 'foo': ('function', ['ax'], [('var', 'pf', ('function', ['ax'], [('return', ('binop', ('identifier', 'ax'), '+', ('identifier', 'ax')))])), ('return', ('identifier', 'pf'))], (None, {...}))}))

"""



