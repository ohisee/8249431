# -*- coding: UTF-8 -*-

from basehandler import BaseHandler;
from xml.dom import minidom;
import urllib2;
import json;

def get_first_child_item(element, tagname):
    try:
        if element and len(element) > 0:
            el = element[0].getElementsByTagName(tagname);
            if el and len(el) > 0 and el[0].firstChild and el[0].firstChild.nodeValue:
                return el[0].firstChild.nodeValue;
    except:
        return None;
    
def get_child_item(element, tagname):
    try:
        if element:
            el = element.getElementsByTagName(tagname);
            if el and len(el) > 0 and el[0].firstChild and el[0].firstChild.nodeValue:
                return el[0].firstChild.nodeValue;
    except:
        return None;


def read_news_info():
    try:
        NEWS_URL = "http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml"
        p_xml = urllib2.urlopen(NEWS_URL);
        p_dom_xml = minidom.parseString(p_xml.read());
        channel = p_dom_xml.getElementsByTagName("channel");
        title = get_first_child_item(channel, "title");
        pubdate = get_first_child_item(channel, "pubDate");
        items = p_dom_xml.getElementsByTagName("item");
        return (title, pubdate, items);
    except:
        return None;

#
#
#
class FetchInfoHandler(BaseHandler):   
    def get(self):
        news = {};
        MAX_LEN = 25;
        news_items = read_news_info();
        if news_items and len(news_items) > 2:
            news["feed"] = news_items[0];
            news["date"] = news_items[1];
            items = news_items[2];
            items_len = len(items) if len(items) <= MAX_LEN else MAX_LEN;
            result = [{"title" : get_child_item(items[i], "title")} for i in range(items_len)];
            news["items"] = result if result else [{"empty" : "empty"}];
            
        self.setJsonHeader();
        self.write(json.dumps(news));
        