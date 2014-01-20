#!/usr/bin/python

import sys

oldKey = None
highestSale = 0

# Loop around the data
# It will be in the format key\tval
# Where key is the store name, val is the sale amount
#
# All the sales for a particular store will be presented,
# then the key will change and we'll be dealing with the next store
#
# Update to find highest sales number of each separate store 

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisSale = data_mapped

    if oldKey and oldKey != thisKey:
        print oldKey, "\t", highestSale;
        oldKey = thisKey;
	highestSale = 0;

    oldKey = thisKey
    tempSale = float(thisSale);
    if highestSale <= tempSale:
	highestSale = tempSale;

if oldKey != None:
    print oldKey, "\t", highestSale;

