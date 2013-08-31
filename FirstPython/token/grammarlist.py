# Bank Heist
#
# Suppose you are a daring thief who has infiltrated the palace of an evil
# dictator. You need to be quick when making your escape, so you can only
# carry 20 kilograms of unbroken goods out with you. Despite this, you want
# to escape with items worth as much money as possible. Suppose further
# that there are three artifacts available:
#
#       a 1502 ACE Incan statue massing 15 kilograms, valued at $30000 
#       a 1499 ACE Aztec jade mask massing 9 kilograms, valued at $16000
#       a 300 ACE Mayan urn massing 8 kilograms, valued at $15000
#
# It is not possible to take all three, and even though the Incan statue
# has the highest value-to-mass ratio, given a 20 kilogram limit the best
# choice is to take the Aztec mask and the Mayan urn.
#
# This is the setup for the "0-1 Knapsack Problem", an important task in
# theoretical computer science. In general, deciding what to take given a
# list of items and a mass limit is believed to be very difficult. This
# question does not ask you to come up with a solution, however -- instead,
# you will evaluate solutions.
#
# We can encode a problem instance as follows. We'll use a dictionary
# mapping item names to (mass,value) pairs.  
#
available = {
        "statue" : (15, 30000) ,
        "mask" : (9, 16000) ,
        "urn" : (8, 15000) ,
} 
#
# Then the mass limit and the taken objects are just a number and a
# string list respectively: 
limit = 20
taken = [ "mask", "urn" ] 
#
# Write a Python procedure heistvalid(available,limit,taken) that returns
# True (the boolean value True, not the string "True") if the objects
# in the list `taken' have a total mass less than or equal to the limit.
#
# In addition, write a Python procedure heisttotal(available,limit,taken)
# that returns the total value (as a number) of the objects in the list 
# `taken'. 
#
# This problem is meant to provide practice for *list comprehensions*. Make
# the body each of your procedures *at most one line long*. 
#
# Hint: sum([1,2,3]) == 6 

def heistvalid(available, limit, taken):
    return sum([available[t][0] for t in taken if t in available]) <= limit;

def heisttotal(available, limit, taken):        
    return sum([available[t][1] for t in taken if t in available]);
    
# We have provided some test cases. You will likely want to make others.
#print heistvalid(available, limit, taken) == True
#print heisttotal(available, limit, taken) == 31000
#print heisttotal(available, limit, taken)
#allthree = ["statue", "mask", "urn"] 
#print heistvalid(available, limit, allthree) == False
#print heisttotal(available, limit, allthree) == 61000


# Common Ground
#
# Consider the strings "Tapachula" and "Temapache", both of which name
# towns in the country of Mexico. They share a number of substrings in
# common. For exmaple, "T" and "pa" can be found in both. The longest
# common unbroken substring that they both share is "apach" -- it starts
# at position 1 in "Tapachula" and at position 3 in "Temapache". Note that
# "Tapach" is not a substring common to both: even though "Temapache"
# contains both "T" and "apach", it does not contain the unbroken substring
# "Tapach". 
#
# Finding the longest common substring of two strings is an important
# problem in computer science. It is a building block to related problems,
# such as "sequence alignment" or "greatest common subsequence" that are
# used in problem domains as diverse as bioinformatics and making spelling
# checkers. 
#
# We will use memoization, recursion and list comprehensions to tackle this
# problem. In particular, we will build up a chart that stores computed
# partial answers. 
#
# To make the problem a bit easier, we'll start by computing the longest
# common *suffix* of two strings. For example, "Tapachula" and "Temapache"
# have no common suffix -- or a common suffix of length 0, if you prefer.
# By contrast, "Tapach" and "Temapach" have a longest common suffix of
# length 5 ("apach"). One way to reason to that is that their last letters
# match (an "h" in both cases) -- and if you peel those last letters off
# the smaller problem of "Temapac" vs. "Tapac" has a common suffix of size
# four. 
#
# Write a memoized procedure csuffix(X,Y) that returns the size of the
# longest common suffix of two strings X and Y. This is 0 if X and Y have
# different final letters. Otherwise, it is 1 plus csuffix() of X and Y,
# each with that common last letter removed. Use a global dictionary chart
# that maps (X,Y) pairs to their longest common suffix values to avoid
# recomputing work. If either X or Y is the empty string, csuffix(X,Y) must
# return 0. 
#
# Once we have csuffix(), we can find the largest common substring of X and
# Y by computing the csuffix() of all possible combinations of *prefixes*
# of X and Y and returning the best one. Write a procedure prefixes(X) that
# returns a list of all non-empty strings that are prefixes of X. For
# example, prefixes("cat") == [ "c", "ca", "cat" ]. 
#
# Finally, write a procedure lsubstring(X,Y) that returns the length of the
# longest common substring of X and Y by considering all prefixes x of X
# and all prefixes y of Y and returning the biggest csuffix(x,y)
# encountered. 

# Hint 1. Reminder: "hello"[-1:] == "o"
#
# Hint 2. Reminder: "goodbye"[:-1] == "goodby" 
#
# Hint 3. prefixes(X) can be written in one line with list comprehensions.
# Consider "for i in range(len(X))". 
#
# Hint 4. max([5,-2,8,3]) == 8
#
# Hint 5. You can "comprehend" two lists at once! 
#       [ (a,b) for a in [1,2] for b in ['x','y'] ]
#               == [(1, 'x'), (1, 'y'), (2, 'x'), (2, 'y')]
# This is by no means necessary, but it is convenient.

chart = { }
def csuffix(X,Y):
    if (X, Y) in chart:
        return chart[(X, Y)];
    else:
        result = 0;
        if len(X) > 0 and len(Y) > 0 and X[-1:] == Y[-1:]:
            result = 1 + csuffix(X[:-1], Y[:-1]);
        chart[(X, Y)] = result;
        return result;

def prefixes(X):
    return [X[0:i] for i in range(1, len(X) + 1)];
        

def lsubstring(X,Y):
    return max([csuffix(r, q) for r in prefixes(X) for q in prefixes(Y)]);

# We have included some test cases. You will likely want to write your own.

print (csuffix('chat', 'hat'), chart);
print (prefixes('chat'));
print ([(r, q) for r in prefixes('chat') for q in prefixes('hat')])

print lsubstring("Tapachula", "Temapache") == 5  # Mexico, "apach"
print chart[("Tapach","Temapach")] == 5
print lsubstring("Harare", "Mutare") == 3        # Zimbabwe, "are" 
print chart[("Harare","Mutare")] == 3
print lsubstring("Iqaluit", "Whitehorse") == 2   # Canada, "it" 
print chart[("Iqaluit","Whit")] == 2
print lsubstring("Prey Veng", "Svay Rieng") == 3 # Cambodia, "eng" 
print chart[("Prey Ven","Svay Rien")] == 2
print chart[("Prey Veng","Svay Rieng")] == 3
print lsubstring("Aceh", "Jambi") == 0           # Sumatra, ""
print chart[("Aceh", "Jambi")] == 0

#print (prefixes('chat'));
#print (csuffix('chat', 'hat'));
#print (lsubstring("Tapachula", "Temapache"))
#print (chart[("Tapach","Temapach")])

# Define a variable regexp that matches numbers with 1 or more leading digits
# and an optional . followed by 0 or more digits.

import re;

regexp = r"[0-9]+\.?[0-9]*";
#regexp = r"[0-9]+(?:\.[0-9]*)?";

tests = [("123", True), ("1.2", True), ("1.", True), (".5", False), (".5.6", False), ("1..2", False)]

for r, ans in tests:
    print (re.findall(regexp, r) == [r]) == ans
    
print ('testing re');

# Learning Regular Expressions

# Define a variable regexp that matches the left 3 strings but not the right 3.

#   Yes     No
#   aaa    aabbb
#   abb    aaccc
#   acc     bc

regexp = r"a(?:aa|bb|cc)"
regexp = r"a+(?:(?:bb)|(?:cc))?"

tests = [("aaa", True), ("abb", True), ("acc", True), ("aabbb", False), ("aaccc", False), ("bc", False)]

for r, ans in tests:
    #print (re.findall(regexp, r))
    print (re.findall(regexp, r) == [r]) == ans
    
    
# List Comprehensions

# Write a short Python program that for all numbers x between 0 and 99 prints
# x^3 (x*x*x), but only if x is even and x^3 < 20.

def cubic():
    return [x*x*x for x in range(100) if (x % 2 == 0) and (x*x*x < 20)];

print (cubic());