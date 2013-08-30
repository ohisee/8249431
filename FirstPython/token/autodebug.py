# CHALLENGE: Automatic Debugging
#
# A key part of debugging is minimizing test cases to localize defects. We
# want the smallest test case possible that is still "interesting". For
# example, suppose we start with a too-big JavaScript test case:
#
#       var x = 1;
#       var y = 2;
#       var z = 3;
#       x = y + z; 
#       y = z; 
#       z = x + x; 
#
# And further suppose that the bug in question triggers on any addition
# involving defined variables. In that case, both of these two smaller test
# cases are also "interesting": 
#
#       var x = 1;
#       var y = 2;
#       var z = 3;
#       x = y + z; 
#
# And:
#
#       var x = 1;
#       var z = 3;
#       z = x + x; 
#
# We want to find the smallest test case we can that still shows the bug
# (i.e., is still "interesting"). One way to do this is to manually remove
# lines and check to see if the result is still interesting. But that is
# time consuming! Why don't we just write a program to do that for us? 
#
# We'll represent a test case as a list. For example, our test case above
# might be: 
#
test1 = [ ("var","x"),                  # var x 
          ("var","y"),                  # var y 
          ("var","z"),                  # var z 
          ("add",["x","y","z"]),        # x = y + z
          ("set",["y","z"]),            # y = z 
          ("add",["z","x","x"]), ]      # z = x + x 
#
# To see if a test case is still "interesting", we would run our program on
# it and look for errors or crashes or whatnot. We'll abstract that by
# assuming that we have a function call interesting(test) that takes as
# input a test case and returns true if it is interesting. For example:
#
def interesting1(test):
    # The test is interesting if it contains "A + B" on some line
    # and "var A" and "var B" _before_ that line. Let's hack something
    # up that simulates that. 
    for i in range(len(test)):
        line = test[i] 
        if line[0] == "add":
            if line[1] == [x for x in line[1] if ("var",x) in test[:i]]:
                return True 
    return False 
#
# Your task is to write a function autodebug(test,interesting). It returns a
# smallest subset (sublist) of test such that that subset is makes
# interesting returns true. "Smallest" is measured by list length. 
# You may assume that that input test is interesting. 
# 
# Hint: Compose "find all subsets" with "find max". 

def gen_sub_list(remaining, showed):
    if not remaining:
        return [showed];
    else:
        ns = [] + showed;
        ns.append(remaining[0]);
        return gen_sub_list(remaining[1:], ns) + gen_sub_list(remaining[1:], showed);

def subsets(lst):
    result = [[]];
    for elt in lst:
        temp = [] + result;
        for sub in temp:
            result.append(sub + [elt]);
    return result;

def autodebug(test, interesting): 
    # find the smallest subset of test that is still interesting!
    if not interesting(test):
        return None
    # your code here ...
    sub_lists = subsets(test);
    return min([interesting_lst for interesting_lst in sub_lists if interesting(interesting_lst)], key = len);

# We have written a few test cases. You may want to include others, but
# keep them small to spare our servers. 

print autodebug(test1, interesting1) ==  [('var', 'x'), ('var', 'z'), ('add', ['z', 'x', 'x'])]
print ('testing')
print (autodebug(test1, interesting1));
print (gen_sub_list(test1, []));
print ("elements");
for el in gen_sub_list(test1, []):
    if interesting1(el):
        print el;
print ("elements");    
for el in subsets(test1):
    if interesting1(el):
        print el;

def interesting2(lst):
    # For this one, a list is interesting if it contains three numbers
    # in strict ascending order. 
    for i in range(len(lst)):
        for j in range(i):
            for k in range(j):
                if lst[k] < lst[j] and lst[j] < lst[i]:
                    return True
    return False

# Random numbers
test2 = [ 2270, 10193, 10149, 32125, 18656, 2275, 1548, 3418, 13155, 25667, 9520, 4896, 10667 ]  
#
#ans = autodebug(test2, interesting2) 
#print len(ans) == 3
#print interesting2(ans);
print interesting2(test2);
print (autodebug(test2, interesting2));


oo = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
print oo[:5];


# Write a procedure that accepts a list as an argument. The procedure should
# print out all of the subsets of that list.
lst = ['a', 'b', 'c'];
def get_sub_list(remaining, showed):
    #print ('remaining %s' % remaining);
    #print ('showed %s' % showed);
    
    if not remaining:
        print ('no more remaining');
        #if showed is not None:
        print (showed);
        return showed;
    else:
        showed.append(remaining[0]);
        #print ('calling invite 1');
        get_sub_list(remaining[1:], showed);
        print ('invite 1 result:')
        #print ('-------------------------------------- %s' % r);
        #print ('calling invite 2');
        print (remaining);
        print (showed);
        showed.pop();
        get_sub_list(remaining[1:], showed);
        #print ('invite 2 result');
        #print ('-------------------------------------- %s' % r);
        
def sub_list(lst):
    get_sub_list(lst, []);

#print ('hello');
#sub_list(lst);
#print ('hello again')
#print (gen_sub_list(test1, []));

print (gen_sub_list(['a', 'b', 'c'], []));
print (subsets(['a', 'b', 'c']));