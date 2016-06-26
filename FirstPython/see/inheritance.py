'''
'''
class Dish(object):
    """
    Represents a food dish.
    """

    def __init__(self, name, price, description=None, vegetarian=False):
        self.name = name
        self.price = price
        self.description = description
        self.vegetarian = vegetarian
    
    def __str__(self):
        return "{name}{isveg}: {price:.2f}{desc} {extras}".format(
            name=self.name,
            desc=' (' + self.description + ')' if self.description else '',
            price=self.price,
            isveg='*' if self.vegetarian else '',
            extras = self.extras())
   
class MainDish(Dish):
    """
    Represents an entree (main dish).
    """
    pass
    def __init__(self, name, price, description=None, vegetarian=False, sides=None):
        super(MainDish, self).__init__(name, price, description, vegetarian);
        self.sides = sides;
        #self = super(MainDish, self).extras();
     
    '''   
    def __str__ (self):
        return "{main} {sides}".format(main = super(MainDish, self).__str__(), sides = "Sides: " + str(self.sides) if self.sides else '');
    '''
    def extras(self):
        return "{sides}".format(sides = "Sides: " + str(self.sides) if self.sides else '');
    
class Appetizer(Dish):
    """
    Represents an appetizer.
    """
    pass
    def __init__(self, name, price, description=None, vegetarian=False, serves=None):
        super(Appetizer, self).__init__(name, price, description, vegetarian);
        self.serves = serves;
        #self = super(Appetizer, self).extras();

    '''
    def __str__ (self):
        return "{main} {serves}".format(main = super(Appetizer, self).__str__(), serves = "Serves: " + str(self.serves) if self.serves else '');
    '''
    def extras(self):
        return "{serves}".format(serves = "Serves: " + str(self.serves) if self.serves else '');                                     