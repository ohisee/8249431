# -*- coding: UTF-8 -*-

from basehandler import BaseHandler;
from xml.dom import minidom;
import urllib2;
import json;

def read_news_info():
    try:
        NEWS_URL = "http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml"
        p_xml = urllib2.urlopen(NEWS_URL);
        p_dom_xml = minidom.parseString(p_xml.read());
        items = p_dom_xml.getElementsByTagName("item");
        return items;
    except:
        return None;

#
#
#
class FetchInfoHandler(BaseHandler):   
    def get(self):
        result = [];
        MAX_LEN = 25;
        items = read_news_info();
        if items:
            items_len = len(items) if len(items) <= MAX_LEN else MAX_LEN;
            for i in range(items_len):
                ti = items[i].getElementsByTagName("title");
                if len(ti) >= 1:
                    t = ti[0];
                    if t and t.firstChild and t.firstChild.nodeValue is not None:
                        result.append({"title" : t.firstChild.nodeValue});
        
        if not result:
            result.append({"empty" : "empty"});
        
        self.setJsonHeader();
        self.write(json.dumps({"items" : result}));
        