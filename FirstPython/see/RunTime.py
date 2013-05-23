import time;
import urllib;

def time_execution (code):
    start = time.clock();
    result = eval(code);
    run_time = time.clock() - start;
    return result, run_time;


def spin_loop (n):
    i = 0;
    while (i < n):
        i = i + 1;
        
        
#print (10 ** 4);

from see.Restaurant import Restaurant;
lunch = Restaurant('asdddddd', 'w', 's');
'''
def another_yummy():
    return True;
lunch.is_yummy = another_yummy;
print (lunch.is_yummy());
'''
print (lunch.name);
lunch.name = "something";
print (lunch);

from see.Dish import DiscerningBear, Human;
dave = Human("Dave");
bob = Human("Bob");
dave.climb_tree();
bob.climb_tree();

fussy = DiscerningBear("Fussy");
fussy.chase(bob);
fussy.chase(dave);

from see.bear import DiscerningBlackBear;
mortimer = DiscerningBlackBear("Mortimer");
print (mortimer.name);

from see.inheritance import Appetizer;
friedpython = Appetizer("Fried Python", 101.30, serves=23)
print (friedpython);