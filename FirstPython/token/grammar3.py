# Memofibo

# Submit via the interpreter a definition for a memofibo procedure that uses a
# chart. You are going to want the Nth value of the chart to hold the Nth
# fibonacci number if you've already computed it and to be empty otherwise.

def fibonacci(n):
    if n == 0:
        return 0;
    elif n == 1:
        return 1;
    else:
        return fibonacci(n - 1) + fibonacci(n - 2);
    
chart = {}

def memofibo(n):
    if n in chart:
        return chart[n];
    else:
        if n == 0:
            chart[0] = 0;
            return 0;
        elif n == 1:
            chart[1] = 1;
            return 1;
        else:
            r = memofibo(n - 1) + memofibo(n - 2);
            chart[n] = r;
            return r;
    
import time;
import timeit;

def time_execution (code):
    start = time.clock();
    result = eval(code);
    run_time = time.clock() - start;
    return result, run_time;


result, run_time = time_execution("memofibo(25)");

print ("the first computation result is %d and took %f seconds" % (result, run_time));

result, run_time = time_execution("memofibo(25)");

print ("the second computation result is %d and took %f seconds" % (result, run_time));

t = timeit.Timer(stmt = """ 
chart = {}
def memofibo(n):
    if n in chart:
        return chart[n];
    else:
        if n == 0:
            chart[0] = 0;
            return 0;
        elif n == 1:
            chart[1] = 1;
            return 1;
        else:
            r = memofibo(n - 1) + memofibo(n - 2);
            chart[n] = r;
            return r;
            
memofibo(25)

""");

print (t.timeit(number=100));

# Addtochart

# Let's code in Python! Write a Python procedure addtochart(chart,index,state)
# that ensures that chart[index] returns a list that contains state exactly
# once. The chart is a Python dictionary and index is a number. addtochart
# should return True if something was actually added, False otherwise. You may
# assume that chart[index] is a list.


def addtochart(chart, index, state):
    if index in chart:
        r = chart[index];
        if state in r:
            return False;
        else:
            r.append(state);
            return True;
    else:
        chart[index] = [state];
        return True;
    
t = [1, 2, 3, 4, 4, 5, 6, 7, 7,];
print (set(t));
print (t);
chart = {1: ['A']}
print (addtochart(chart, 1, 'B'));
print (chart);

# Writing Closure

# We are currently looking at chart[i] and we see x => ab . cd from j

# Write the Python procedure, closure, that takes five parameters:

#   grammar: the grammar using the previously described structure
#   i: a number representing the chart state that we are currently looking at
#   x: a single nonterminal
#   ab and cd: lists of many things

# The closure function should return all the new parsing states that we want to
# add to chart position i

# Hint: This is tricky. If you are stuck, do a list comphrension over the grammar rules.

def closure (grammar, i, x, ab, cd):
    return [];


grammar = [ 
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ("t",["I","like","t"]),
    ("t",[""])
    ]

print closure(grammar,0,"exp",["exp","+"],["exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
print closure(grammar,0,"exp",[],["exp","+","exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
print closure(grammar,0,"exp",["exp"],["+","exp"]) == []
