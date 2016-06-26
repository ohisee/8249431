'''
Implementation of Memoization

# Define a procedure, cached_execution(cache, proc, proc_input), that takes in
# three inputs: a cache, which is a Dictionary that maps inputs to proc to
# their previously computed values, a procedure, proc, which can be called by
# just writing proc(proc_input), and proc_input which is the input to proc.
# Your procedure should return the value of the proc with input proc_input,
# but should only evaluate it if it has not been previously called.

'''

# start cache as an empty dictionary
cache = {};

def factorial(n):
    print ("Running factorial");
    result = 1;
    for i in range(2, n + 1):
        result = result * i;
    return result;


def cached_execution(cache, proc, proc_input):
    key_proc = "Proc_" + str(proc);
    key_input = "Proc_input_" + str(proc_input);
    Input = "Input";
    Value = "Value";
    add_key = False;
    
    if key_proc in cache:
        if key_input not in cache[key_proc]:
            add_key = True;
        else:
            return cache[key_proc][key_input][Value];
    
    result = proc(proc_input);
    if add_key:
        cache[key_proc][key_input] = {Input : proc_input, Value: result};
    else:
        cache[key_proc] = {key_input : {Input : proc_input, Value: result}};
    return result;

def cached_fibo(n):
    if n == 1 or n == 0:
        return n
    else:
        return (cached_execution(cache, cached_fibo, n - 1 )
               + cached_execution(cache, cached_fibo, n - 2 ))

# print (cached_execution(cache, factorial, 10));
# print (cache);
# print (cached_execution(cache, factorial, 9));
# print (cache);
# print (cached_execution(cache, factorial, 10));
# print (cached_execution(cache, factorial, 10));
# print (cached_execution(cache, factorial, 10));
# print (cached_execution(cache, factorial, 10));
# print (cached_execution(cache, factorial, 10));
# print (cached_execution(cache, factorial, 10));
# print (cache);

import time

# complex_computation() simulates a slow function. time.sleep(n) causes the
# program to pause for n seconds. In real life, this might be a call to a
# database, or a request to another web service.
def complex_computation(a, b):
    time.sleep(1)
    return a + b

# QUIZ - Improve the cached_computation() function below so that it caches
# results after computing them for the first time so future calls are faster

def cached_computation(a, b):
    key = "%s%s" % (a, b);
    if key in cache:
        r = cache[key];
    else:
        r = complex_computation(a, b);
        cache[key] = r;
    return r;
        

start_time = time.time()
#print (cached_computation(5, 3))
#print ("the first computation took %f seconds" % (time.time() - start_time))

start_time2 = time.time()
#print (cached_computation(5, 3))
#print ("the second computation took %f seconds" % (time.time() - start_time2))

SERVERS = ['SERVER1', 'SERVER2', 'SERVER3', 'SERVER4']

# QUIZ - implement the function get_server, which returns one element from the
# list SERVERS in a round-robin fashion on each call. Note that you should 
# comment out all your 'print get_server()' statements before submitting 
# your code or the grading script may fail.

n = -1
def get_server():
    global n;
    n = (n + 1) % len(SERVERS);
    return SERVERS[n];

# print get_server()
# print get_server()
# print get_server()
# print get_server()
# print get_server()
# print get_server()
# print get_server()
# print get_server()

# QUIZ implement the basic memcache functions

CACHE = {}

#return True after setting the data
def set1(key, value):
    if key:
        CACHE[key] = value;
        return True;
    return False;
        

#return the value for key
def get(key):
    return CACHE.get(key);

#delete key from the cache
def delete(key):
    if key in cache:
        del CACHE[key];

#clear the entire cache
def flush():
    CACHE.clear();

print set1('x', 1)
#>>> True

print get('x')
#>>> 1

print get('y')
#>>> None
delete('x')
print get('x')
#>>> None

# QUIZ - implement gets() and cas() below
#return a tuple of (value, h), where h is hash of the value. a simple hash
#we can use here is hash(repr(val))
def gets(key):
    val = get(key);
    if val:
        return (val, hash(repr(val)));
    return None;

# set key = value and return True if cas_unique matches the hash of the value
# already in the cache. if cas_unique does not match the hash of the value in
# the cache, don't set anything and return False.
# def cas(key, value, cas_unique):
#     hs = gets(key);
#     if hs and cas_unique == hs[1]:
#         return set1(key, value);
#     return False;

def cas(key, value, cas_unique):
    hs = gets(key);
    if hs:
        val, hu = hs;
        if cas_unique == hu:
            return set1(key, value);
    return False;