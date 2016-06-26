'''
'''
from google.appengine.ext import db;

#
# Build blog key
#
def blogUserParentKey(name = 'default'):
    return db.Key.from_path('BlogUsers', name);

#
# Get user by ID - created by key
#
def getBlogUserByUserId(userid):
    key = db.Key.from_path("BlogUser", userid, parent = blogUserParentKey());
    return db.get(key);

class BlogUser(db.Model):
    user_name = db.StringProperty(required = True);
    user_email = db.StringProperty(required = False);
    user_password = db.StringProperty(required = True);
    user_created = db.DateTimeProperty(auto_now_add = True);
    user_last_signed_in = db.DateTimeProperty(auto_now = True);
    user_reg_last_modified = db.DateTimeProperty(auto_now = True);
    
    def toString(self):
        return "{user};{email};{pw};{created};{lastsign};{lastmodified}".format(user = self.user_name, 
                                                                           email = self.user_email, 
                                                                           pw = self.user_password,
                                                                           created = self.user_reg_last_modified,
                                                                           lastsign = self.user_last_signed_in,
                                                                           lastmodified = self.user_reg_last_modified);
    @classmethod
    def findByUsername(cls, username):
        bu = BlogUser.all().filter('user_name =', username).get();
        return bu;
    
    @classmethod
    def validUser(cls, username, password):
        bu = cls.findByUsername(username);
        if bu and bu.user_password == password:
            return bu;
        return None;
    