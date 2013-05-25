'''
'''

from datetime import datetime;

class WikiPage(object):
    def __init__(self, wiki_text, url_path):
        self.wiki_text = wiki_text;
        self.url_path = url_path;
        self.version = 1;
        self.created_date = datetime.utcnow();
        
    #
    # Return first 100 characters
    #
    def get_wiki_text(self):
        return self.wiki_text[0:100];
    
    def get_url_path(self):
        return self.url_path;
    
    def get_version(self):
        return self.version;
    
    def set_wiki_version(self, version):
        if version:
            self.version = version;
    
    def set_style(self, style):
        self.style = style;
    
    def same_path(self, url_path):
        return self.url_path == url_path;
    
    def get_created_date(self):
        return self.created_date.strftime('%a %B %d %H:%M:%S %Y');
        
    @classmethod
    def sortWikiPage(cls, lst):
        lst.sort(key = lambda wiki: wiki.created_date);
        return lst;
    
    @classmethod
    def reverseWikiPage(cls, lst):
        lst.reverse();
        return lst;
        