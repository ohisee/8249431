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
        return [showed];
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

print ('hello');
sub_list(lst);
print ('hello again')
print (gen_sub_list(lst, []));
        