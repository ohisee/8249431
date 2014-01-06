import re;

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
