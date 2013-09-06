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
    return [ (g[0], [], g[1], i) for g in grammar if cd and cd[0] == g[0]];



grammar = [ 
    ("exp", ["exp", "+", "exp"]),
    ("exp", ["exp", "-", "exp"]),
    ("exp", ["(", "exp", ")"]),
    ("exp", ["num"]),
    ("t",["I","like","t"]),
    ("t",[""])
    ]

#print closure(grammar,0,"exp",["exp","+"],["exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
#print closure(grammar,0,"exp",[],["exp","+","exp"]) == [('exp', [], ['exp', '+', 'exp'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['num'], 0)]
#print closure(grammar,0,"exp",["exp"],["+","exp"]) == []

print closure(grammar,0,"exp",["exp"],["+","exp"]);


# Writing Shift

# We are currently looking at chart[i] and we see x => ab . cd from j. The input is tokens.

# Your procedure, shift, should either return None, at which point there is
# nothing to do or will return a single new parsing state that presumably
# involved shifting over the c if c matches the ith token.

def shift (tokens, i, x, ab, cd, j):
    if cd and len(tokens) >= i and cd[0] == tokens[i]:
        return (x, ab + [cd[0]], cd[1:], j);
    else:
        return None;

#print shift(["exp","+","exp"],2,"exp",["exp","+"],["exp"],0) == ('exp', ['exp', '+', 'exp'], [], 0)
#print shift(["exp","+","exp"],0,"exp",[],["exp","+","exp"],0) == ('exp', ['exp'], ['+', 'exp'], 0)
#print shift(["exp","+","exp"],3,"exp",["exp","+","exp"],[],0) == None
#print shift(["exp","+","ANDY LOVES COOKIES"],2,"exp",["exp","+"],["exp"],0) == None

print ('testing');
print shift(["exp","+","exp"],2,"exp",["exp","+"],["exp"],0);

o = ['exp'];
print (o[0]);
oo = ["exp","+","ANDY LOVES COOKIES"];
print (len(oo));


# Writing Reductions

# We are looking at chart[i] and we see x => ab . cd from j.

# Hint: Reductions are tricky, so as a hint, remember that you only want to do
# reductions if cd == []

# Hint: You'll have to look back previously in the chart. 

chart = {0: [('exp', ['exp'], ['+', 'exp'], 0), ('exp', [], ['num'], 0), ('exp', [], ['(', 'exp', ')'], 0), ('exp', [], ['exp', '-', 'exp'], 0), ('exp', [], ['exp', '+', 'exp'], 0)], 
         1: [('exp', ['exp', '+'], ['exp'], 0)], 
         2: [('exp', ['exp', '+', 'exp'], [], 0)]}

def reductions(chart, i, x, ab, cd, j):
    if len(cd) == 0 and j in chart:
        states = chart[j];
        return [(state[0], state[1] + [state[2][0]], state[2][1:], state[3]) for state in states if state[2] and state[2][0] == x];
    else:
        return [];
             
#print reductions(chart,2,'exp',['exp','+','exp'],[],0) == [('exp', ['exp'], ['-', 'exp'], 0), ('exp', ['exp'], ['+', 'exp'], 0)]
print ('testing...')
print (reductions(chart,2,'exp',['exp','+','exp'],[],0));

param_grammar = [ 
    ("S", ["P"]),           # S -> P
    ("P", ["(", "P", ")"]), # P -> ( P )
    ("P", []),              # P ->
    ]
tokens = ["(", "(", ")", ")", ]

def parse(tokens, grammar):
    tokens = tokens + ["end_of_input_marker"];
    chart = {};
    start_rule = grammar[0]; # for example, S -> P
    for i in range(len(tokens) + 1):
        chart[i] = [];
    start_state = (start_rule[0], [], start_rule[1], 0);
    chart[0] = [ start_state ];
    for i in range(len(tokens)):
        while True:
            changes = False;
            for state in chart[i]:
                # State === x -> ab . cd, j
                x = state[0];
                ab = state[1];
                cd = state[2];
                j = state[3];
                
                # Closure
                # Current State ==   x -> a b . c d , j
                # Option 1: For each grammar rule c -> p q r
                # (where the c's match)
                # make a next state               c -> . p q r , i
                # English: We're about to start parsing a "c", but
                #  "c" may be something like "exp" with its own
                #  production rules. We'll bring those production rules in.
                next_states = closure(grammar, i, x, ab, cd);
                for next_state in next_states:
                    changes = addtochart(chart, i, next_state) or changes;
                    
                # Shift
                # Current State ==   x -> a b . c d , j
                # Option 2: If tokens[i] == c,
                # make a next state               x -> a b c . d , j
                # in chart[i+1]
                # English: We're looking for to parse token c next
                #  and the current token is exactly c! Aren't we lucky!
                #  So we can parse over it and move to j+1.
                next_state = shift(tokens, i, x, ab, cd, j);
                if next_state is not None:
                    changes = addtochart(chart, i + 1, next_state) or changes;
                    
                # Reduction
                # Current State ==   x -> a b . c d , j
                # Option 3: If cd is [], the state is just x -> a b . , j
                # for each p -> q . x r , l in chart[j]
                # make a new state                p -> q x . r , l
                # in chart[i]
                # English: We just finished parsing an "x" with this token,
                #  but that may have been a sub-step (like matching "exp -> 2"
                #  in "2+3"). We should update the higher-level rules as well.
                next_states = reductions(chart, i, x, ab, cd, j);
                for next_state in next_states:
                    changes = addtochart(chart, i, next_state) or changes;
            
            # We are done if nothing changed       
            if not changes:
                break;
            
    # Print out parsing state(s)
    for i in range(len(tokens)):
        print ("=== chart %s" % str(i));
        for state in chart[i]:
            x = state[0];
            ab = state[1];
            cd = state[2];
            j = state[3];
            print ("   %s  ->" % x),
            for sym in ab:
                print (" %s" % sym),
            print (" ."),
            for sym in cd:
                print (" %s" % sym), 
            print ("  from %s" % str(j));
                
    accepting_state = (start_rule[0], start_rule[1], [], 0)
    return accepting_state in chart[len(tokens) - 1];
    
print ("chart -------");
result = parse(tokens, param_grammar);
print (result);

param_grammar2 = [
        ("S", ["E"]),
        ("E", ["(", "E", ")"]),
        ("E", ["E", "+", "E"]),
        ("E", ["E", "-", "E"]),
        ("E", ["id", "(", "A", ")"]),
        ("E", ["id"]),
        ("A", ["NA"]),
        ("A", []),
        ("NA", ["E"]),
        ("NA", ["E", ",", "NA"]),
        ]
tokens2 = ["id", "(", "(", "id", ")", ",", "id", ")"];
result = parse(tokens2, param_grammar2);
print (result);