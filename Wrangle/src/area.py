#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = '../citiesinfobox.csv'

def is_int(value):
    try:
        int (value);
        return True;
    except ValueError:
        return False;
    
def is_float(value):
    try:
        float (value);
        return True;
    except ValueError:
        return False;
    
def count_non_zero(value):
    return sum([1 for d in value if d in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]]);
    
def extract_area(area):
    t = area[1:-1];
    a, b = t.split("|");
    af = count_non_zero("%s" % float(a));
    bf = count_non_zero("%s" % float(b));
    return float(a) if af > bf else float(b);


def fix_area(area):

    # YOUR CODE HERE
    if area is None or area == "NULL" or area == "":
        area = None;
    elif is_float(area):
        area = float(area);
    elif area.startswith("{"):
        area = extract_area(area);
    else:
        area = None;
                        
    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()
            
        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,9):
        print n;
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55166700.0
    assert data[3]["areaLand"] == None


if __name__ == "__main__":
    test()