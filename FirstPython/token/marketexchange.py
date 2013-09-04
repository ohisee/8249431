# Market Exchange
#
# Focus: Units 5 and 6, Interpreting and Environments
#
#
# In this problem you will use your knowledge of interpretation and
# environments to simulate a simple market. Here the "program" is not a
# list of JavaScript commands that describe webpage computation, but
# instead a list of economic commands that describe business transactions.  
#
# Our parse tree (or abstract syntax tree) is a list of elements. Elements
# have three forms: has, buy and sell. "has" elements indicate that the
# given person begins with the given amount of money:
#
#       [ "klaus teuber", "has", 100 ] 
#
# "buy" elements indicate that the given person wants to purchase some
# item for the listed amount of money. For example:
#
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#
# ... means that "klaus teuber" is interesting in buying the item
# "sheep" for 50 monetary units. For this assignment, that transaction will
# only happen if there is a seller also selling "sheep" for 50 (and if
# klaus actually has 50 or more monetary units). That is, both the item and
# the price must match exactly. The final type of element is "sell": 
#
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#
# This indicates that "andreas seyfarth" is willing to sell the item
# "sheep" for 50 monetary units. (Again, that transaction will only take
# place if there is a buyer wishing to purchase that item for exactly the
# same amount of money -- and if the buyer actually has at least that much
# money!) 
#
# All of the "has" commands will come first in the program.
#
# "buy" and "sell" elements only operate once per time they are listed. In
# this example: 
# 
#       [ "klaus teuber", "has", 100 ] 
#       [ "andreas seyfarth", "has", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#
# klaus will buy "sheep" from andreas once, at which poin klaus will have
# 50 money and andreas will have 100. However, in this example:
#
#       [ "klaus teuber", "has", 100 ] 
#       [ "andreas seyfarth", "has", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ] 
#       [ "klaus teuber", "buy", "sheep", 50 ]          # listed twice
#       [ "andreas seyfarth", "sell", "sheep" , 50 ] 
#       [ "andreas seyfarth", "sell", "sheep" , 50 ]    # listed twice
# 
# klaus will buy "sheep" from andreas and then buy "sheep" from andreas
# again, at which point klaus will have 0 money and andreas will have 150. 
#
# Write a procedure evaluate() that takes a list of elements as an input.
# It should perform all possible transactions, in any order, until no more
# transactions are possible (e.g., because all "buy" and "sell" elements
# have been used and/or potential buyers do not have enough money left for
# their desired "buy"s). Your procedure should return an environment
# (a Python dictionary) mapping names to final money amounts (after all
# transactions have happened).  
#
# Hint: To avoid processing a "buy" or "sell" twice, you might either call
# yourself recursively with a smaller AST (i.e., with those two elements
# removed) or you can use Python's list.remove() to remove elements "in
# place". Example: 
#
# lst = [("a",1) , ("b",2) ]
# print lst
# [('a', 1), ('b', 2)]
# 
# lst.remove( ("a",1) )
# print lst
# [('b', 2)]

def evaluate_has(name, amount, env):
    env[name] = amount;

def evaluate_buy(buyer, item, amount, buying_env):
    buying_env.append((buyer, item, amount));
    
#
# The buyer must have >= the amount of money, and the buy price must == the sell price.
# 
# Start processing seller(s) from end of selling list. This is for instance when first selling 
# attempt fails to be processed due to less buying amount and moving onto next / second selling 
# attempt which allows the buyer to earn enough to complete the first selling transaction.
#
def evaluate_sell(seller, item, amount, has_amount_env, buying_env, selling_env):
    selling_env.append((seller, item, amount));
    for selling_item in selling_env[::-1]:
        s_seller = selling_item[0];
        s_item = selling_item[1];
        s_amount = selling_item[2];
        for buying_item in buying_env:
            buyer = buying_item[0];
            b_item = buying_item[1];
            b_amount = buying_item[2];
            if s_item == b_item:
                if buyer in has_amount_env:
                    existing_amount = has_amount_env[buyer];
                    if existing_amount >= s_amount and s_amount == b_amount:
                        has_amount_env[buyer] = existing_amount - s_amount;
                        buying_env.remove(buying_item);
                        if s_seller in has_amount_env:
                            has_amount_env[s_seller] = has_amount_env[s_seller] + s_amount;
                            selling_env.remove(selling_item);
                        
def evaluate(ast):
    # fill in your code here ...
    transactions = {"has": {}, "buy" : [], "sell" : []};
    for elt in ast:
        if elt[1] == "has":
            evaluate_has(elt[0], elt[2], transactions["has"]);
        if elt[1] == "buy":
            evaluate_buy(elt[0], elt[2], elt[3], transactions["buy"]);
        if elt[1] == "sell":
            evaluate_sell(elt[0], elt[2], elt[3], transactions["has"], transactions["buy"], transactions["sell"]);
    return transactions["has"];


# In test1, exactly one sell happens. Even though klaus still has 25 money
# left over, a "buy"/"sell" only happens once per time it is listed. 
test1 = [ ["klaus","has",50] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test1) == {'klaus': 25, 'wrede': 105}
print evaluate(test1);

# In test2, klaus does not have enough money, so no transactions take place.
test2 = [ ["klaus","has",5] ,
          ["wrede","has",80] ,
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , ] 

print evaluate(test2) == {'klaus': 5, 'wrede': 80}

# Wishful thinking, klaus! Although you want to buy sheep for 5 money and
# you even have 5 money, no one is selling sheep for 5 money. So no
# transactions happen.
test2b = [ ["klaus","has",5] ,
           ["wrede","has",80] ,
           ["klaus","buy","sheep", 5] ,
           ["wrede","sell","sheep", 25] , ] 

print evaluate(test2b) == {'klaus': 5, 'wrede': 80}

# In test3, wrede does not have the 75 required to buy the wheat from
# andreas until after wrede sells the sheep to klaus. 
test3 = [ ["klaus","has",50] ,
          ["wrede","has",50] ,
          ["andreas","has",50] ,
          ["wrede","buy","wheat", 75] ,
          ["andreas","sell","wheat", 75] , 
          ["klaus","buy","sheep", 25] ,
          ["wrede","sell","sheep", 25] , 
          ] 
print evaluate(test3 ) == {'andreas': 125, 'klaus': 25, 'wrede': 0}
print evaluate(test3 );

test4 = [['klaus', 'has', 150], 
         ['wrede', 'has', 150], 
         ['andreas', 'has', 150], 
         ['wrede', 'buy', 'wheat', 76], 
         ['andreas', 'sell', 'wheat', 75]
         ]
print evaluate(test4);
