# -*- coding: UTF-8 -*-
#
# This is a model class for blog
#
import json;
from google.appengine.ext import db;

#
# Build blog key
#
def blogParentKey(name = 'default'):
    return db.Key.from_path('Blogs', name);

#
# Get blog by ID - created by key
#
def getBlogByPostId(post_id):
    key = db.Key.from_path("Blog", post_id, parent = blogParentKey());
    return db.get(key);

#
# Blog entity model
#
class Blog(db.Model):
    blog_subject = db.StringProperty(required = True);
    blog_text = db.TextProperty(required = True);
    blog_created = db.DateTimeProperty(auto_now_add = True);
    blog_last_modified = db.DateTimeProperty(auto_now = True);
    
    def build(self, uri, blog_id):
        self._blog_link_text = "{link}{keyId}".format(link = uri, keyId = blog_id);
        self._subject_text = self.blog_subject;
        self._render_text = self.blog_text.replace('\n', '<br/>');
        self._date_text = self.blog_created.strftime("%B %d, %Y");
        return self;
    
    def get_id_link(self, uri):
        return "{link}{keyId}".format(link = uri, keyId = self.key().id());
    
    def get_subject_text(self):
        return self.blog_subject;
    
    def get_blog_text(self):
        return self.blog_text.replace('\n', '<br/>');
    
    def get_created_date_text(self):
        return self.blog_created.strftime("%B %d, %Y");
    
    def get_blog_text_json(self):
        return self.blog_text;
    
    def get_blog_subject_json(self):
        return self.blog_subject;
    
    def get_blog_created_json(self):
        return self.blog_created.strftime("%a %b %d %H:%M:%S %Y");
    
    def get_blog_last_modified_json(self):
        return self.blog_last_modified.strftime("%a %b %d %H:%M:%S %Y");
    
    def prepare_blog(self):
        return {'content' : self.get_blog_text_json(),
                'created' : self.get_blog_created_json(),
                'last_modified' : self.get_blog_last_modified_json(),
                'subject' : self.get_blog_subject_json()};
    
    def dumps_blog_into_json(self):
        blog_json = json.dumps(self.prepare_blog());
        return blog_json;
    
    @classmethod
    def retrieveBlogs(cls, count = None):
        bl = Blog.all().order('-blog_created');
        if count and count.isdigit():
            return json.dumps([be.prepare_blog() for be in bl.fetch(limit = count)]);
        else:
            return json.dumps([be.prepare_blog() for be in bl]);
            
            
            