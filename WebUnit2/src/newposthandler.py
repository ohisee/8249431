#
# New post handler
#
from google.appengine.ext import db;
from google.appengine.api import memcache;
from basehandler import BaseHandler;
from blogmodel import Blog, blogParentKey, getBlogByPostId;
from datetime import datetime;


def flushCache():
    return memcache.flush_all();

def setCacheAge(key, val):
    memcache.set(key, (val, datetime.utcnow()));
    
def getCacheAge(key):
    val = memcache.get(key);
    if val:
        bl, lastStart = val;
        return bl, (datetime.utcnow() - lastStart).total_seconds();
    return None, 0;
    
#
# Cache blog list front page
# QUERIED = re.compile("(?i)Queried\s+(\d+)(\.\d+)?\s+seconds?\s+ago")
#
def cacheBlogList(update = False):
    blogListKey = "blogListKey";
    
    blogList, lastStart = getCacheAge(blogListKey);
    if update or blogList is None:
        blogList = db.GqlQuery("SELECT * FROM Blog WHERE ANCESTOR IS :1 ORDER BY blog_created DESC limit 10", 
                               blogParentKey());
        blogList = list(blogList);
        setCacheAge(key = blogListKey, val = blogList);
    
    return blogList, lastStart;
                            
#
# Cache blog entry
#
def cacheBlogEntry(blog_id, update = False):
    blogKey = 'blog_%s' % blog_id;
    
    blogEntry, lastStart = getCacheAge(blogKey);
    if update or blogEntry is None:
        blogEntry = getBlogByPostId(int(blog_id));
        if blogEntry:
            setCacheAge(key = blogKey, val = blogEntry);
            return blogEntry, lastStart;
        return None, 0;
    
    return blogEntry, lastStart;

def cacheNewBlogEntry(blog_id, blogentry):
    blogKey = 'blog_%s' % blog_id;
    setCacheAge(key = blogKey, val = blogentry);

def buildAgeStr(age):
    s = 'Queried %d seconds ago';
    if int(age) == 1:
        s = s.replace('seconds', 'second');
    return s % age;
    
   
'''
/blog/newpost
'''
class NewPostHandler(BaseHandler):
    def get(self):
        self.render("newblogpost-form.html");
        
    def post(self):
        blog_subject = self.request.get("subject");
        blog_text = self.request.get("content");
        have_error = False;
        error_text = '';
        
        param = dict(subject = blog_subject, content = blog_text);
        
        if not blog_subject:
            error_text += "Missing subject, please enter a subject.";
            param['error'] = error_text;
            have_error = True;
            
        if not blog_text:
            error_text += "\nMissing blog text, please enter some blog texts."
            param['error'] = error_text;
            have_error = True;
            
        if have_error:
            self.render("newblogpost-form.html", **param);
        else:
            #parent must be lower case
            new_post_blog = Blog(parent = blogParentKey(), blog_subject = blog_subject, blog_text = blog_text);
            new_post_blog.put();
            cacheBlogList(True);
            cacheNewBlogEntry(new_post_blog.key().id(), new_post_blog);
            self.redirect('/blog/%s' % str(new_post_blog.key().id()) );

'''
/blog/?
'''
class ListBlogHandler(BaseHandler):    
    def get(self):
        bloglist, lastStart = cacheBlogList();
        self.render("blogpost.html", bloglist = bloglist, age = buildAgeStr(lastStart));

'''
/blog/([0-9])+
/blog/([0-9])+.json
Update to minimize DB query
'''
class BlogLinkPageHandler(BaseHandler):
    def get(self, blog_id):
        blog, lastStart = cacheBlogEntry(blog_id);
        if blog:
            self.render('ablogcontent.html', blogentry = blog, age = buildAgeStr(lastStart));
        else:
            self.error(500);
            return;

'''
/blog/([0-9])+.json
'''
class BlogLinkJsonHandler(BaseHandler):
    def get(self, blog_id):
        blog = getBlogByPostId(int(blog_id));
        if blog:
            self.setJsonHeader();
            self.write(blog.dumps_blog_into_json());
        else:
            self.error(500);
            return;

'''
/blog/.json
'''       
class ListBlogJsonHandler(BaseHandler):
    def get(self):
        self.setJsonHeader();
        self.write(Blog.retrieveBlogs());
        
'''
/blog/flush
'''       
class flushHandler(BaseHandler):
    def get(self):
        flushCache();
        self.redirect('/blog');