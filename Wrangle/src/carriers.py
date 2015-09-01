#!/usr/bin/python
# -*- coding: utf-8 -*-

# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI
# All your changes should be in the 'extract_carrier' function
# Also note that the html file is a stripped down version of what is actually on the website.

# Your task in this exercise is to get a list of all airlines. Exclude all of the combination
# values, like "All U.S. Carriers" from the data that you return.
# You should return a list of codes for the carriers.

from bs4 import BeautifulSoup
import requests
import json
import urllib2

html_page = "../options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html);
        
        carrierlist = soup.find(id="CarrierList");
        if carrierlist:
            options = carrierlist.find_all("option");
            for option in options:
                value = option.get("value");
                if value and value not in ["All", "AllForeign", "AllUS"]:
                    data.append(value);

    return data

# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"
def extract_airports(page):
    data = []
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html);
        
        airpostlist = soup.find(id="AirportList");
        if airpostlist:
            options = airpostlist.find_all("option");
            for option in options:
                value = option.get("value");
                if value and value not in ["All", "AllMajors", "AllOthers"]:
                    data.append(value);

    return data;


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': airport,
                          'CarrierList': carrier,
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data
    
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()