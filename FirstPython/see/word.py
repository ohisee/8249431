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

D = re.compile(r"[0-9]");
print (D.match('05'));

print (re.findall(r"[0-9]", "Mir Taqi 1723"));
print (re.findall(r"[a-z][0-9]", "a1 2b cc3 44d"));
print (re.findall(r"[0-9][ ][0-9]+", "a1 2b cc3 44d"));

