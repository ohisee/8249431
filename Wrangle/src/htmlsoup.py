#!/usr/bin/python
# -*- coding: utf-8 -*-

# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the approprate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
from bs4 import BeautifulSoup
import requests
import json
import urllib2

html_page = "page_source.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    #with open(page, "r") as html:
        # do something here to find the necessary values
        # pass
    url = "http://www.transtats.bts.gov/Data_Elements.aspx?Data=2";
    resp = urllib2.urlopen(url);
    html = resp.read();
    
    soup = BeautifulSoup(html);
        
    eventval = soup.find(id="__EVENTVALIDATION");
    if eventval:
        value = eventval.get("value");
        if value:
            data["eventvalidation"] = value;
            
                
    viewstate = soup.find(id="__VIEWSTATE");
    if viewstate:
        value = viewstate.get("value");
        if value:
            data["viewstate"] = value;
    
    return data


def make_request(data):
    #eventvalidation = data["eventvalidation"]
    #viewstate = data["viewstate"]
    
    s = requests.Session();
    
    r = s.get("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2");
    
    soup = BeautifulSoup(r.text);
    
    eventval = soup.find(id="__EVENTVALIDATION");
    if eventval:
        value = eventval.get("value");
        if value:
            data["eventvalidation"] = value;
            
                
    viewstateval = soup.find(id="__VIEWSTATE");
    if viewstateval:
        value = viewstateval.get("value");
        if value:
            data["viewstate"] = value;
            
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_data(html_page)
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")

    
test()