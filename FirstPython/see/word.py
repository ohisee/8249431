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