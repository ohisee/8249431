#!/usr/bin/python

# Format of each line is:
# 10.82.30.199 - - [29/Jul/2009:08:56:19 -0700] "GET /trailers/ HTTP/1.1" 200 11508
# IP address - - [dd/Mon/year:hh:mm:ss -nnnn] "GET | POST uri HTTP/1.1 or 1.0" HTTP status code size
#
# We need to write them out to standard output, separated by a tab

import sys;
import os;
import re;
from urlparse import urlparse;

REG = r'(?P<host>\S+).*"(?P<request>.+)"';

for line in sys.stdin:
    data = re.findall(REG, line.strip());
    if data and len(data) > 0:
	ip, request = data[0];
	page = request.split();
	if page and len(page) > 1:
	    f = urlparse(page[1]);
	    if f.path and len(f.path) > 0:
		fname = os.path.basename(f.path);
	    	print "{0}\t{1}".format(fname, f.path);
