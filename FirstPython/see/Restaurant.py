'''
a class
'''

class Restaurant (object):
    """
    Represent a place that serves food
    """    
    def __init__(self, name, owner, chef):
        """
        """
        self.name = name;
        self.owner = owner;
        self.chef = chef;
        
    def __str__ (self):
        """
        """
        return self.name + " (Owner: " + self.owner + ", Chef: " + self.chef + ")";
    
    def display (self):
        """
        Prints out information about this restaurant
        """
        print (self.name);
        
    def is_yummy (self):
        """
        a method
        """
        return False;