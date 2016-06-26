#
# Base Handler class
# 

import os;
import webapp2;
import jinja2;
from validate import check_secure_val, make_secure_val;

template_dir = os.path.join(os.path.dirname(__file__), 'templates');
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True);

class BaseHandler(webapp2.RequestHandler):    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template);
        return t.render(params);
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw);
    
    def render(self, template, **templateArgs):
        self.write(self.render_str(template, **templateArgs));
        
    def deleteCookie(self, cookie_name):
        self.response.headers.add_header('Set-Cookie', '%s=; Path=%s' % (str(cookie_name), '/'));
        
    def setSecureCookie(self, cookie_name, cookie_val):
        new_cookie_val = make_secure_val(cookie_val);
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=%s' % (str(cookie_name), str(new_cookie_val), '/'));
        
    def validateSecureCookie(self, cookie_name):
        cookie_val = self.request.cookies.get(str(cookie_name));
        return check_secure_val(cookie_val);
    
    def setJsonHeader(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8';
