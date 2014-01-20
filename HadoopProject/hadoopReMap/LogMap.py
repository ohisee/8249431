import re;
from os.path import basename;
from urlparse import urlparse;

logentry = """127.0.0.1 user-identifier user [10/Oct/2000:13:55:36 -0700] "GET /access/ HTTP/1.0" 200 2326""";

reg = r'(?P<host>\S+).*"(?P<request>.+)"';

regr = r'(?:GET|POST)\s+\/.*\s+HTTP/\d{1}.\d{1}';

data = re.findall(reg, logentry.strip());
print (data);
if data and len(data) > 0:
    ip, request = data[0];
    page = request.split();
    if page and len(page) > 2:
        print ("{0}\t{1}".format(ip, page[1]));


logentry = """127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /set/picture/loop.jp HTTP/1.0" 200 2326""";

reg = r'"(?P<request>.+)"';

regr = r'(?:GET|POST)\s+\/.+\s+HTTP/\d{1}.\d{1}';

def extract_filename ():
    req = re.findall(reg, logentry);
    if req:
        p = req[0].split();
        if p and len(p) > 2:
            page = p[1];
            f = urlparse(page);
            print f.path, "\t", f.params, "\t", f.query;
            if f.path and len(f.path) > 0:
                fname = basename(f.path);
                print "file name : %s" % fname;

extract_filename();