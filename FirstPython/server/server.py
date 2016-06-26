'''
'''

import web;

from see.search import lucky_search;
from see.crawler import crawl_web_using_sets, compute_ranks;

class LuckySearch(object):
    def GET(self, query):
        return lucky_search(corpus, ranks, query);
    
class About(object):
    def GET(self, query):
        return "This is my udacious project!";
    
corpus, graph = crawl_web_using_sets("http://udacity.com/cs101x/urank/index.html");
ranks = compute_ranks(graph);
app = web.application(('/about', 'About', '/(.*)', 'LuckySearch'), globals());
app.run();