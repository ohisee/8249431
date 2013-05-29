#
# New post handler
#
from google.appengine.ext import db;
from google.appengine.api import memcache;
from basehandler import BaseHandler;
from blogmodel import Blog, blogParentKey, getBlogByPostId;
from datetime import datetime;
from wikipage import WikiPage;


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

#
# Cache wiki text
#
def cacheWikiStr(url, wiki_text, update = False):
    wiki_key = "wiki_key_%s" % url;
    wiki_content, lastStart = getCacheAge(wiki_key);
    if update or wiki_content is None:
        if wiki_text:
            setCacheAge(key = wiki_key, val = wiki_text);
    return wiki_content;

def findWikiByUrl(url):
    wiki_key = "wiki_lst_key_%s" % url;
    wiki_lst, lastStart = getCacheAge(wiki_key);
    return wiki_key, wiki_lst;

MOST_VERSION = 30;
def cacheWiki(url, wiki, v = None):
    wiki_key, wiki_lst = findWikiByUrl(url);
    
    if wiki_lst is None:
        if wiki and wiki.wiki_text:
            wiki_lst = [wiki];
            setCacheAge(key = wiki_key, val = wiki_lst);
    else:            
        if wiki and wiki.wiki_text:
            if v:
                if str(v).isdigit():
                    v = int(v);
                    if v > 0 and v <= len(wiki_lst):
                        wiki.set_wiki_version(v);
                        wiki_lst[v - 1] = wiki;
                        setCacheAge(key = wiki_key, val = wiki_lst);
            else:
                ver = len(wiki_lst);
                wiki.set_wiki_version(ver + 1);
                wiki_lst.append(wiki);
                setCacheAge(key = wiki_key, val = wiki_lst);

        wiki_lst.reverse();
    
    return wiki_lst;

def getWikiByUrlVersion(url, version):
    wiki_key, wiki_lst = findWikiByUrl(url);
    if wiki_lst:
        # 1. version must be a string of digit and 
        # less than or equal to 2 characters long 
        # to avoid long string of characters.
        # 2. version must start at 1.
        if str(version).isdigit() and len(version) <= 2:
            v = int(version);
            if v > 0 and v <= len(wiki_lst):
                return wiki_lst[v - 1];
    return None;
    

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
        #blog = getBlogByPostId(int(blog_id));
        blog, lastStart = cacheBlogEntry(blog_id);
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
class FlushHandler(BaseHandler):
    def get(self):
        flushCache();
        self.redirect('/blog');
        
'''
Arbitrary URL to trigger wiki with login
'''
class WikiPageHandler(BaseHandler):
    def get(self, random_url):
        wiki_text = cacheWikiStr(random_url, '');
        if self.user:
            version = self.request.get('v');
            ev_link = '/wiki/_edit%s' % random_url;
            if version:
                wiki = getWikiByUrlVersion(url = random_url, version = version);
                if not wiki:
                    return self.pageNotfound();
                wiki_text = wiki.get_wiki_text();
                ev_link = '/wiki/_edit%s?v=%s' % (random_url, version);

            if wiki_text:
                params = dict(loggedin = True, wiki_text = wiki_text, username = self.user.user_name, ev = 'edit', 
                              ev_link = ev_link, logout_link = '/logout', history = '/wiki/_history%s' % random_url);
                self.render('wiki-display.html', **params);
            else:
                self.redirect('/wiki/_edit%s' % random_url);
        else:
            if wiki_text:
                params = dict(loggedin = False, wiki_text = wiki_text, login_link = '/login', 
                              signup_link = '/signup', history = '/wiki/_history%s' % random_url);
                self.render('wiki-display.html', **params);
            else:
                self.redirect('/wiki/_edit%s' % random_url);
    
class WikiPageLogoutHandler(BaseHandler):
    def get(self):
        next_url = self.nextUrl();
        self.logout();
        self.redirect(next_url);

class EditWikiHandler(BaseHandler):
    def get(self, random_url):
        if self.user:
            wiki_text = cacheWikiStr(random_url, '');
            version = self.request.get('v');
            view_url = random_url;
            if version:
                wiki = getWikiByUrlVersion(url = random_url, version = version);
                if not wiki:
                    return self.pageNotfound();
                wiki_text = wiki.get_wiki_text();
                view_url = '%s?v=%s' % (random_url, version);

            self.render('wiki-form.html', wiki_text = wiki_text if wiki_text else '', ev_link = view_url, 
                        username = self.user.user_name, history = '/wiki/_history%s' % random_url, 
                        logout_link = '/logout');
        else:
            self.redirect('/login');
                            
        
    def post(self, random_url):
        if self.user:
            wiki_text = self.request.get('wiki_text');
            version = self.request.get('v');
            redirect_url = random_url;
            if wiki_text:
                pre_wiki_text = cacheWikiStr(random_url, '');
                if version:
                    pre_wiki = getWikiByUrlVersion(url = random_url, version = version);
                    if pre_wiki and pre_wiki.wiki_text:
                        pre_wiki_text = pre_wiki.wiki_text;
                    redirect_url = '%s?v=%s' % (random_url, version);
                    
                if wiki_text != pre_wiki_text:
                    cacheWikiStr(random_url, wiki_text, True);
                    cacheWiki(random_url, WikiPage(wiki_text = wiki_text, url_path = random_url), version);
            
            self.redirect(redirect_url);
        else:
            self.error(500);
            return;
        
class WikiPageHistoryHandler(BaseHandler):
    def get(self, path):
        if self.user:
            wiki_lst = cacheWiki(path, None);
            if wiki_lst:
                self.render('wiki-history.html', loggedin = True, wikilst = wiki_lst, view_link = path +'?v=%s',
                            update_link = '/wiki/_edit' + path + '?v=%s', 
                            username = self.user.user_name, logout_link = '/logout');
        else:
            self.redirect('/login');