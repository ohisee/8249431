#!/usr/bin/python

# Format of each line is:
# 10.82.30.199 - - [29/Jul/2009:08:56:19 -0700] "GET /trailers/ HTTP/1.1" 200 11508
# IP address - - [dd/Mon/year:hh:mm:ss -nnnn] "GET | POST uri HTTP/1.1 or 1.0" HTTP status code size
#
# We need to write them out to standard output, separated by a tab

import sys;
import re;

REG = r'(?P<host>\S+).*"(?P<request>.+)"';

for line in sys.stdin:
    data = re.findall(REG, line.strip());
    if data and len(data) > 0:
	ip, request = data[0];
	page = request.split();
	if page and len(page) > 1:
	    print "{0}\t{1}".format(ip, page[1]);
