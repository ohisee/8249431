#
# Sign up handler extends base handler
#

from basehandler import BaseHandler;
from validate import valid_username, valid_password, valid_email;
from usermodel import BlogUser, blogUserParentKey;
   
'''
/unit2/signup
/blog/signup
'''
class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup-form.html");
        
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");
        verify = self.request.get("verify");
        email = self.request.get("email");
        have_error = False
        
        params = dict(username = username, email = email);

        if not valid_username(username):
            params['error_username'] = "That's not a valid username.";
            have_error = True;
        elif BlogUser.findByUsername(username):
            params['error_username'] = "That user already exists.";
            have_error = True;

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password.";
            have_error = True;
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match.";
            have_error = True;

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True;
        
        if have_error:
            self.render('signup-form.html', **params);
        else:
            new_user = BlogUser(parent = blogUserParentKey(username), 
                                user_name = username, user_email = email, user_password = password);
            new_user.put();
            self.setSecureCookie('user_id', username)
            self.redirect('/blog/welcome');
            
    
'''
/blog/login
/login
''' 
class LoginHandler(BaseHandler):
    def get(self):
        next_url = self.request.headers.get('referer', '/');
        self.render("login-form.html", next_url = next_url);
    
    def post(self):
        username = self.request.get("username");
        password = self.request.get("password");
        have_error = False;
        next_url = str(self.request.get('next_url'));
        if not next_url:
            next_url = '/blog/welcome';
        
        params = dict(username = username, password = password);
        
        login_user = BlogUser.validUser(username, password);
        if not login_user:
            params['error_login'] = "Invalid login";
            have_error = True;
            
        if have_error:
            self.render('login-form.html', **params);
        else:
            self.login(username);
            self.redirect(next_url);
 
            
'''
/blog/logout
''' 
class LogoutHandler(BaseHandler):
    def get(self):
        self.logout();
        self.redirect('/blog/signup');   
                     
'''
/unit2/welcome
/blog/welcome
'''
class WelcomeHandler(BaseHandler):
    def get(self):
        username_val = self.validateSecureCookie('user_id')
        if username_val:
            self.render('welcome.html', username = username_val);
        else:
            self.redirect('/blog/signup');
