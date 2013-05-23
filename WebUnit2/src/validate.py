#
# Validate user name, password, email, cookie
#

import hashlib;
import hmac;
import re;
import random;
import string;

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username);

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password);

# \S A non-whitespace character
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email);

COOKIE_RE = re.compile(r'.+=;\s*Path=/')
def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)

SECRET = 'imsosecret';
def hash_str(s):
    #return hashlib.md5(s).hexdigest();
    return hmac.new(SECRET, s).hexdigest();

# Use | instead of . because of an issue in app engine
def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s));

# Use | instead of . because of an issue in app engine
def check_secure_val(h):
    t = h.split('|');
    if len(t) == 2:
        return t[0] if h == make_secure_val(t[0]) else None;
    else:
        return None;
    
# Make salt for password
def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5));

# Make password with salt
def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt();
    hashinput = "%s%s%s" % (name, pw, salt);
    hashpw = "%s,%s" % (hashlib.sha256(hashinput).hexdigest(), salt);
    return hashpw;

def valid_pw(name, pw, h):
    t = h.split(',');
    if len(t) == 2:
        return h == make_pw_hash(name, pw, t[1]);
    return False;