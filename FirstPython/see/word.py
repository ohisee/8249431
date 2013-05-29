print ("Ada Lovelace".find(" "));
print ("Alan Turing".find("n", 4));

def myfirst_yoursecond(p,q):
    pi = p.find(" ");
    qi = q.find(" ");
    if pi != -1 and qi != -1:
        return p[0:pi] == q[qi + 1:];
    return False;

print (myfirst_yoursecond("bell hooks", "curer bell"));

