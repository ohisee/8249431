'''
Bear
'''

class Bear(object):
    def __init__(self, name):
        """
        init of bear
        """
        self.name = name;
        
class BlackBear(Bear):
    def __init__(self, name):
        super(BlackBear, self).__init__("Black " + name);
        
class PandaBear(Bear):
    def __init__(self, name):
        super(PandaBear, self).__init__("Panda " + name);
        
class DiscerningBear(Bear):
    def __init__(self, name):
        super(DiscerningBear, self).__init__("Discerning " + name);
        
class DiscerningBlackBear(DiscerningBear, PandaBear, BlackBear):
    """
    """
    
if __name__ == '__main__':
    
    bb = DiscerningBlackBear('abc');
    print (bb.name);
