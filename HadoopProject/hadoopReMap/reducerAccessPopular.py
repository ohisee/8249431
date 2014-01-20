#!/usr/bin/python

import sys

popularCount = 0;
addrCount = 0;
oldAddr = None;
popularAddress = None;

# Loop around the data
# It will be in the format key\tval
# Where key is the store name, val is the sale amount

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisAddr, thisPath = data_mapped

    if oldAddr and oldAddr != thisAddr:
	if addrCount > popularCount:
	    popularCount = addrCount;
	    print oldAddr, "\t", popularAddress, "\t", popularCount;
	oldAddr = thisAddr;
        addrCount = 0;

    oldAddr = thisAddr;
    popularAddress = thisPath;
    addrCount += 1;

if oldAddr != None:
    if addrCount >= popularCount:
	popularCount = addrCount;
	print oldAddr, "\t", popularAddress, "\t", popularCount;

print oldAddr, "\t", popularAddress, "\t", popularCount;
