print ("Ada Lovelace".find(" "));
print ("Alan Turing".find("n", 4));

def myfirst_yoursecond(p,q):
    pi = p.find(" ");
    qi = q.find(" ");
    if pi != -1 and qi != -1:
        return p[0:pi] == q[qi + 1:];
    return False;

print (myfirst_yoursecond("bell hooks", "curer bell"));

print (len("Python is fun".split()));
print (len("July-August 1842".split()));
print (len("6*9==42".split()));

import re;

#D = re.compile(r"[0-9]");
#print (D.match('05'));

#print (re.findall(r"[0-9]", "Mir Taqi 1723"));
#print (re.findall(r"[a-z][0-9]", "a1 2b cc3 44d"));
#print (re.findall(r"[0-9][ ][0-9]+", "a1 2b cc3 44d"));
#print (re.findall(r"[a-z]+|[0-9]+", "Havel1936"));
#regexp = r"ab|[0-9]+";
#print (re.findall(regexp,"ab"));
#print (re.findall(regexp,"1"));

# Assign to the variable regexp a Python regular expression that matches
# lowercase words (a-z) or singly-hyphenated lowercase words.
#regexp = r"[a-z]+\-[a-z]+|[a-z]+";
#print (re.findall(regexp,"well-liked"));
#print (re.findall(regexp,"html"));
#print (re.findall(regexp,"i"));

# Assign to the variable regexp a Python regular expression that matches single-
# argument mathematical functions.
# The function name is a lowercase word (a-z), the function argument must be a
# number (0-9), and there may optionally be spaces before and/or after the
# argument.
# Hint: You may need to escape the ( and ).
#regexp = r"[a-z]+\([\s]*[0-9]+[\s]*\)";
#print (re.findall(regexp,"cos(0)"));
#print (re.findall(regexp,"sqrt(   2     )"));
#print (re.findall(regexp,"cos     (0)"));

# Assign to regexp a regular expression for double-quoted string literals that
# allows for escaped double quotes.
# Hint: Escape " and \
# Hint: (?: (?: ) )
#regexp = r"\"(?:[^\\][^\"].+)|(?:[\\\"](?:.+)[\\\"])+\"";
#regexp = r'"(?:[^\\]|(?:\\.))*"'
#regexp = r"\"(?:[^\\][^\"])+|(?:[\\\"](?:.+)[\\\"])+\"";
#print (re.findall(regexp,'"I say, \\"hello.\\" \\"hello.\\""'));
#print (re.findall(regexp,'"\\"'));


# Finite state machine simulator
edges = {(1, 'a') : 2, (2, 'a') : 2, (2, '1') : 3, (3, '1') : 3};

accepting = [3];
#string -> regular expression string
#current -> state of FSM
#edges -> input into FSM
#accepting -> accepting state
def fsmsim(string, current, edges, accepting):
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        # QUIZ: You fill this out!
        # Is there a valid edge?
        # If so, take it.
        # If not, return False.
        # Hint: recursion.
        if (current, letter) in edges:
            cs = edges[(current, letter)];
            return fsmsim(string[1:], cs, edges, accepting);
        return False;


print (fsmsim("aaa111",1,edges,accepting));

# FSM Interpretation

# Define edges and accepting to encode r"q*". Name your start state 1.

#edges = {(1, 'q') : 1 }
#
#accepting = [1]

# Define edges and accepting to encode r"[a-b][c-d]?". Name your start state 1.

edges = {(1, 'a') : 2, (1, 'b') : 2, (2, 'c') : 3, (2, 'd') : 3}

accepting = [2, 3]
#
#
#def fsmsim(string, current, edges, accepting):
#    if string == "":
#        return current in accepting
#    else:
#        letter = string[0]
#        if (current, letter) in edges:
#            destination = edges[(current, letter)]
#            remaining_string = string[1:]
#            return fsmsim(remaining_string, destination, edges, accepting)
#        else:
#            return False


# Provide s1 and s2 that are both accepted, but s1 != s2.

s1 = "bdf"

s2 = "bdgbdf"


edges = {(1,'a') : 2,
         (1,'b') : 3,
         (2,'c') : 4,
         (3,'d') : 5,
         (5,'c') : 2,
         (5,'f') : 6,
         (5,'g') : 1}

accepting = [6]


def fsmsim(string, current, edges, accepting):
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        if (current, letter) in edges:
            destination = edges[(current, letter)]
            remaining_string = string[1:]
            return fsmsim(remaining_string, destination, edges, accepting)
        else:
            return False

# Suppose we want to recognize phone numbers with or without hyphens. The
# regular expression you give should work for any number of groups of any (non-
# empty) size, separated by 1 hyphen. Each group is [0-9]+.

# Hint: Accept "5" but not "-6"

#regexp = r"[0-9]+(?:[-]*[0-9]+)+";
#regexp = r"[0-9]+(?:-[0-9]+)*";

#print (re.findall(regexp,"123-4567-123"));
#print (re.findall(regexp,"08-78-88-88-88"));
#print (re.findall(regexp,"0878888888"));
#print (re.findall(regexp,"-6"));

# Title: Summing Numbers

# Write a procedure called sumnums(). Your procedure must accept as input a
# single string. Your procedure must output an integer equal to the sum of
# all integer numbers (one or more digits in sequence) within that string.
# If there are no decimal numbers in the input string, your procedure must
# return the integer 0. The input string will not contain any negative integers.
#
# Example Input: "hello 2 all of you 44"
# Example Output: 46
#
# Hint: int("44") == 44

test_case_input = """The Act of Independence of Lithuania was signed 
on February 16, 1918, by 20 council members."""

#regexp = r"[0-9]+";
#print (re.findall(regexp, test_case_input));

def sumnums(sentence):
    regexp = r"[0-9]+";
    nums = re.findall(regexp, sentence);
    return sum([int(i) for i in nums]);

print (sumnums(test_case_input));

# Singly-Hyphenated Words

# We examined hyphenated words in a quiz in class. In this problem you
# will get a chance to handle them correctly. 
# 
# Assign to the variable regexp a Python regular expression that matches 
# both words (with letters a-z) and also singly-hyphenated words. If you 
# use grouping, you must use (?: and ) as your regular expression
# parentheses. 
#
# Examples: 
#
# regexp exactly matches "astronomy"  
# regexp exactly matches "near-infrared"  
# regexp exactly matches "x-ray"  
# regexp does not exactly match "-tricky" 
# regexp does not exactly match "tricky-" 
# regexp does not exactly match "large - scale" 
# regexp does not exactly match "gamma-ray-burst" 
# regexp does not exactly match "" 

# Your regular expression only needs to handle lowercase strings.

# In Python regular expressions, r"A|B" checks A first and then B - it 
# does not follow the maximal munch rule. Thus, you may want to check 
# for doubly-hyphenated words first and then non-hyphenated words.

regexp = r"(?:[a-z]+-[a-z]+)|(?:[a-z]+)";
test_case_input = """the wide-field-more infrared survey explorer is a nasa
infrared-wavelength space telescope in an earth-orbiting satellite which
performed an all-sky astronomical survey. be careful of -tricky tricky-
hyphens --- be precise."""

#c = re.compile(regexp);
#print (re.findall(regexp, test_case_input));
#c = re.match(regexp, "wide-fielde");
#print (c.groups());

#COOKIE_RE = re.compile(r"(?:[a-z]+-[a-z]+)|(?:[a-z]+)")
#def valid_cookie(cookie):
#    return cookie and COOKIE_RE.match(cookie);
#print (valid_cookie('m-m-mmmmm'));

# Title: Simulating Non-Determinism

# Each regular expression can be converted to an equivalent finite state
# machine. This is how regular expressions are implemented in practice. 
# We saw how non-deterministic finite state machines can be converted to
# deterministic ones (often of a different size). It is also possible to
# simulate non-deterministic machines directly -- and we'll do that now!
#
# In a given state, a non-deterministic machine may have *multiple*
# outgoing edges labeled with the *same* character. 
#
# To handle this ambiguity, we say that a non-deterministic finite state
# machine accepts a string if there exists *any* path through the finite
# state machine that consumes exactly that string as input and ends in an
# accepting state. 
#
# Write a procedure nfsmsim that works just like the fsmsim we covered
# together, but handles also multiple outgoing edges and ambiguity. Do not
# consider epsilon transitions. 
# 
# Formally, your procedure takes four arguments: a string, a starting
# state, the edges (encoded as a dictionary mapping), and a list of
# accepting states. 
#
# To encode this ambiguity, we will change "edges" so that each state-input
# pair maps to a *list* of destination states. 
#
# For example, the regular expression r"a+|(?:ab+c)" might be encoded like
# this:
edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 3],
          (4, 'c') : [5] }
accepting = [2, 5] 
# It accepts both "aaa" (visiting states 1 2 2 and finally 2) and "abbc"
# (visting states 1 3 3 4 and finally 5). 

def nfsmsim(string, current, edges, accepting): 
    if string == "":
        return current in accepting;
    else:
        letter = string[0];
        if (current, letter) in edges:
            states = edges[(current, letter)];
            b = False;
            for state in states:
                b = b or nfsmsim(string[1:], state, edges, accepting);
            return b;
        else:
            return False;
        
#print (nfsmsim("abbbc", 1, edges, accepting));

# Title: Reading Machine Minds

# It can be difficult to predict what strings a finite state machine will
# accept. A tricky finite state machine may not accept any! A finite state
# machine that accepts no strings is said to be *empty*. 
# 
# In this homework problem you will determine if a finite state machine is
# empty or not. If it is not empty, you will prove that by returning a
# string that it accepts. 
#
# Formally, you will write a procedure nfsmaccepts() that takes four
# arguments corresponding to a non-derministic finite state machine:
#   the start (or current) state
#   the edges (encoded as a mapping)
#   the list of accepting states
#   a list of states already visited (starts empty) 
#
# If the finite state machine accepts any string, your procedure must
# return one such string (your choice!). Otherwise, if the finite state
# machine is empty, your procedure must return None (the value None, not
# the string "None"). 
#
# For example, this non-deterministic machine ...
edges = { (1, 'a') : [2, 3],
          (2, 'a') : [2],
          (3, 'b') : [4, 2],
          (4, 'c') : [5] }
accepting = [5] 
# ... accepts exactly one string: "abc". By contrast, this
# non-deterministic machine: 
edges2 = { (1, 'a') : [1],
           (2, 'a') : [2] }
accepting2 = [2] 
# ... accepts no strings (if you look closely, you'll see that you cannot
# actually reach state 2 when starting in state 1). 

# Hint #1: This problem is trickier than it looks. If you do not keep track
# of where you have been, your procedure may loop forever on the second
# example. Before you make a recursive call, add the current state to the
# list of visited states (and be sure to check the list of visited states
# elsewhere). 
#
# Hint #2: (Base Case) If the current state is accepting, you can return
# "" as an accepting string.  
# 
# Hint #3: (Recursion) If you have an outgoing edge labeled "a" that
# goes to a state that accepts on the string "bc" (i.e., the recursive call
# returns "bc"), then you can return "abc". 
#
# Hint #4: You may want to iterate over all of the edges and only consider
# those relevant to your current state. "for edge in edges" will iterate
# over all of the keys in the mapping (i.e., over all of the (state,letter)
# pairs) -- you'll have to write "edges[edge]" to get the destination list. 

edges4 = {(1, 'a'): [2],
          (3, 'b'): [4]}

accepting4 = [4]

#def nfsmaccepts(current, edges, accepting, visited):
#    #print ('Current state %s ' % current);
#    if current in accepting:
#        return "";
#    else:
#        visited = [];
#        visited.append(current);
#        for edge in edges:
#            if current == edge[0]:
#                letter = edge[1];
#                states = edges[edge];
#                #print ('Next States %s' % states);
#                #print ('Letter is %s' % letter);
#                for state in states:
#                    if state not in visited:
#                        r = nfsmaccepts(state, edges, accepting, visited);
#                        if r is not None:
#                            print ('returning %s', (letter + r));
#                            return letter + r;
#                        #return None;
#                    else:
#                        return None;

#edges = {(1,'a') : [2],
#         (1,'b') : [3],
#         (2,'c') : [4],
#         (3,'d') : [5],
#         (5,'c') : [2],
#         (5,'f') : [6],
#         (5,'g') : [1]}
#
#accepting = [6]
       
def nfsmaccepts(current, edges, accepting, visited):
    if current in accepting:
        return "";
    if current in visited:
        return None;
    else:
        visited.append(current);
        for edge in edges:
            if current == edge[0]:
                letter = edge[1];
                states = edges[edge];
                for state in states:
                    if state not in visited:
                        r = nfsmaccepts(state, edges, accepting, visited);
                        if r is not None:
                            return letter + r;
        return None;

print (nfsmaccepts(1, edges, accepting, []));
#print (nfsmaccepts(1, edges, [2], []));
#print (nfsmaccepts(1, edges4, accepting4, []));
                