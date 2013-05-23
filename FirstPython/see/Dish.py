
'''
Dish
'''
class Dish (object):
    '''
    Dish on Menu
    '''

    def __init__(self, name, price, description, picture=None, vegetarian=False):
        '''
        Constructor
        '''
        self.name = name;
        self.price = price;
        self.description = description;
        self.picture = picture;
        self.vegetarian = vegetarian;
        
    def __str__ (self):
        """
        to string
        """
        return "{name} ({desc}: {price:.2f})".format(name=self.name, 
                                                     desc=self.description, 
                                                     price=self.price);

'''
Main Dish
'''
class MainDish(object):
    """
    Represents a food dish.
    """

    def __init__(self, name, price,
                 description=None, picture=None, 
                 vegetarian=False, sides=0):
        self.name = name
        self.price = price
        self.description = description
        self.picture = picture
        self.vegetarian = vegetarian
        self.sides = sides

    def __str__(self):
        return "{name}{isveg}: {price:.2f}{desc}".format(
            name=self.name,
            desc=' (' + self.description + ')' if self.description else '',
            price=self.price,
            isveg='*' if self.vegetarian else '')
    
    
'''
Appetizer
''' 
class Appetizer(object):
    """
    Represents an appetizer.
    """
    def __init__(self, name, price, description=None, picture=None, 
                 vegetarian=False, serves=1):
        # complete this!
        self.name = name;
        self.price = price;
        self.description = description;
        self.picture = picture;
        self.vegetarian = vegetarian;
        self.serves = serves;

    def __str__(self):
        """Returns an appetizer, printed same way as Main Dish"""
        # complete this!
        return "{name}{vegetarian}: {price:.2f}".format(name=self.name, 
                                                        vegetarian = '*' if self.vegetarian == True else '', 
                                                        price=self.price);

'''
Human
'''
class Human(object):
    """Represents a human!"""
    def __init__(self, name):
        self.name = name
        self.up_tree = False

    def climb_tree(self):
        self.up_tree = True

'''
Bear
'''
class Bear(object):
    """Represents a bear!"""
    def __init__(self, name):
        self.name = name

    def eat(self, victim):
        print ("Yummy! " + victim.name + " tastes good...")
    
'''
Grizzly Bear
'''    
class GrizzlyBear(Bear):
    """Represents a GrizzlyBear, which is a type of bear that can knock down trees."""

    def knock_down_tree(self):
        print ("Timber!")

    def chase(self, victim):
        if victim.up_tree:
            self.knock_down_tree()
            victim.up_tree = False
        self.eat(victim)

'''
Discerning Bear
'''        
class DiscerningBear(GrizzlyBear):
    """Represents a DiscerningBear that does not like to eat humans named Dave"""
    pass
    def eat(self, victim):
        if victim.name == "Dave":
            print ("Bleech! I'm not eating {name}!".format(name=victim.name));
        else:
            #print ("Yummy! " + victim.name + " tastes good...");
            super(DiscerningBear, self).eat(victim);