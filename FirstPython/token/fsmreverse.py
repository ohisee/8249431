# Turning Back Time 
#
# Focus: Units 1, 2 and 3: Finite State Machines and List Comprehensions
#
#
# For every regular language, there is another regular language that all of
# the strings in that language, but reversed. For example, if you have a
# regular language that accepts "Dracula", "Was" and "Here", there is also
# another regular language that accepts exactly "alucarD", "saW" and
# "ereH". We can imagine that this "backwards" language is accepted by a
# "backwards" finite state machine.
#
# In this problem you will construct that "backwards" finite state machine. 
# Given a non-deterministic finite state machine, you will write a
# procedure reverse() that returns a new non-deterministic finite state
# machine that accepts all of the strings in the first one, but with their
# letters in reverse order. 
#
# We will use same the "edges" encoding from class, but we
# will make the start and accepting state explicit.  For example, the
# regular expression r"a(?:bx|by)+c" might be encoded like this:

#edges = { (1,'a') : [2],
#          (2,'b') : [3,4],
#          (3,'x') : [5],
#          (4,'y') : [5],
#          (5,'b') : [3,4], 
#          (5,'c') : [6],
#          } 
#accepting = 6 
#start = 1 

# For this problem we will restrict attention to non-deterministic finite
# state machines that have a single start state and a single accepting
# state. Similarly, we will not consider epsilon transitions.
#
# For the example above, since the original NFSM accepts "abxc", the NFSM
# you produce must accept "cxba". Similarly, since the original accepts
# "abxbyc", the NFSM you produce must accept "cybxba", and so on. 
#
# Your procedure "reverse(edges,accepting,start)" should return a tuple
# (new_edges,new_accepting,new_start) that defines a new non-deterministic
# finite state machine that accepts every string in the language of the
# original ... reversed! 
#
# Vague Hint: Draw a picture, and then draw all the arrows backwards. 

def reverse(edges,accepting,start): 
    def reverse_edges(edges, r_accepting, r_start, visited, re_edges):
        if r_start in visited:
            return None;
        elif r_start == r_accepting:
            return None;
        else:
            new_visited = [r_start] + visited;
            for edge in [edge for edge in edges if r_start in edges[edge]]:
                if (r_start, edge[1]) in re_edges and edge[0] not in re_edges[(r_start, edge[1])]:
                    re_edges[(r_start, edge[1])].append(edge[0]);
                else:
                    re_edges[(r_start, edge[1])] = [edge[0]];
                new_r_start = edge[0];
                reverse_edges(edges, r_accepting, new_r_start, new_visited, re_edges);
    
    r_edges = {};
    r_start = accepting;
    r_accepting = start;
    
    reverse_edges(edges, r_accepting, r_start, [], r_edges);
    
    return (r_edges, r_accepting, r_start);
            
                

# We have included some testing code to help you check your work. Since
# this is the final exam, you will definitely want to add your own tests.
#
# Recall: "hello"[::-1] == "olleh" 

edges_reverse = { (6, 'c') : [5],
                  (5, 'x') : [3],
                  (5, 'y') : [4],
                  (4, 'b') : [2,5],
                  (3, 'b') : [2,5],
                  (2, 'a') : [1],
                };

reverse_start = 6;
reverse_accept = 1;
             
edges = { (1,'a') : [2],
          (2,'b') : [3,4],
          (3,'x') : [5],
          (4,'y') : [5],
          (5,'b') : [3,4], 
          (5,'c') : [6],
          #(5,'p') : [6],
          } 

accepting = 6 
start = 1

#r_edges, r_accepting, r_start = reverse(edges,accepting,start);
#print ("testing.....");
#print (r_edges);
#print ([edge for edge in edges if 5 in edges[edge]]);
#
#for edge in [edge for edge in edges if accepting in edges[edge]]:
#    print edge[0], edge[1];

def nfsmaccepts(edges,accepting,current,input_str): 
    if input_str == "":
        return current == accepting;
    letter = input_str[0];
    rest = input_str[1:];
    if (current,letter) in edges:
        for dest in edges[(current,letter)]:
            if nfsmaccepts(edges,accepting,dest,rest):
                return True
    return False
        
#print (nfsmaccepts(edges, accepting, start, "abxbybybxc"));
#print (nfsmaccepts(edges_reverse, reverse_accept, reverse_start, "cxbybybxbxbxbxba"));
        
r_edges, r_accepting, r_start = reverse(edges,accepting,start)
for s in [ "abxc", "abxbyc", "not", "abxbxbxbxbxc", "" ]: 
    # The original should accept s if-and-only-if the
    # reversed version accepts s_reversed. 
    print nfsmaccepts(edges,accepting,start,s) == nfsmaccepts(r_edges,r_accepting,r_start,s[::-1])

# r"a+b*"
edges2 = { (1,'a') : [2],
          (2,'a') : [2],
          (2,'b') : [2] 
          } 
accepting2 = 2 
start2 = 1 

edges3 = { (2, 'a') : [1, 2],
           (2, 'b') : [2],
           #(2, 'a') : [2],
           #(1, 'a') : [1],
         }
e3accepting = 1;
e3start = 2;

#print (nfsmaccepts(edges2,accepting2,start2,'aaaaaaaaaabbbb'));
#print (nfsmaccepts(edges3,e3accepting,e3start,'aaaaaaaaaabbbb'[::-1]));
#r_edges2, r_accepting2, r_start2 = reverse(edges2,accepting2,start2)
#print r_edges2;

r_edges2, r_accepting2, r_start2 = reverse(edges2,accepting2,start2) 

for s in [ "aaaab", "aabbbbb", "ab", "b", "a", "", "ba" ]: 
    print nfsmaccepts(edges2,accepting2,start2,s) == nfsmaccepts(r_edges2,r_accepting2,r_start2,s[::-1])
        
