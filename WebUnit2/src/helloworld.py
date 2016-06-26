#
#
#
import webapp2;

from mainpage import MainPage;
from applyrot13handler import ApplyRot13Handler;
from signuphandler import SignupHandler, WelcomeHandler, LoginHandler, LogoutHandler;
from newposthandler import NewPostHandler, ListBlogHandler, BlogLinkPageHandler, BlogLinkJsonHandler, ListBlogJsonHandler, flushHandler;

app = webapp2.WSGIApplication([('/', MainPage), 
                               ('/unit2/rot13', ApplyRot13Handler),
                               ('/unit2/signup', SignupHandler),
                               ('/blog/signup', SignupHandler),
                               ('/unit2/welcome', WelcomeHandler),
                               ('/blog/welcome', WelcomeHandler),
                               ('/blog/login', LoginHandler),
                               ('/blog/logout', LogoutHandler),
                               ('/blog/?', ListBlogHandler),
                               ('/blog/(?:\.json)?', ListBlogJsonHandler),
                               ('/blog/([0-9]+)', BlogLinkPageHandler),
                               ('/blog/([0-9]+)(?:\.json)?', BlogLinkJsonHandler),
                               ('/blog/flush', flushHandler),
                               ('/blog/newpost', NewPostHandler)],
                              debug=True)