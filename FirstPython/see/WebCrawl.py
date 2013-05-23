

def proc(p):
    #p = p + [1];
    q = p;
    print (q);
    q.append(3);
    print (q);
    q.pop();
    print (q);
    print (p);
    
def ppp (p):
    p.append(123);
    p = p + [1, 2, 3]

def product_list (p):
    result = 1;
    for e in p:
        result = result * e;
    return result; 

def greatest (p):
    result = 0;
    for e in p:
        if (e > result):
            result = e;
    return result;

udacious_univs = [['Udacity',90000,0]]

usa_univs = [ ['California Institute of Technology',2175,37704],
              ['Harvard',19627,39849],
              ['Massachusetts Institute of Technology',10566,40732],
              ['Princeton',7802,37000],
              ['Rice',5879,35551],
              ['Stanford',19535,40569],
              ['Yale',11701,40500], ['Udacity',90000,0]  ]

def total_enrollment(p):
    total_students = 0;
    fee = 0;
    for e in p:
        total_students = total_students + e[1];
        fee = fee + (e[1] * e[2]);
    return total_students, fee;
    

def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return ('<html> <body> This is a test page for learning to crawl! '
            '<p> It is a good idea to '
            '<a href="http://www.udacity.com/cs101x/crawling.html">learn to '
            'crawl</a> before you try to  '
            '<a href="http://www.udacity.com/cs101x/walking.html">walk</a> '
            'or  <a href="http://www.udacity.com/cs101x/flying.html">fly</a>. '
            '</p> </body> </html> ')
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return ('<html> <body> I have not learned to crawl yet, but I '
            'am quite good at '
            '<a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.'
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return ('<html> <body> I cant get enough '
            '<a href="http://www.udacity.com/cs101x/index.html">crawling</a>! '
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return ('<html> <body> The magic words are Squeamish Ossifrage! '
            '</body> </html>')
        elif url == "http://top.contributors/velak.html":
            return ('<a href="http://top.contributors/jesyspa.html">'
        '<a href="http://top.contributors/forbiddenvoid.html">')
        elif url == "http://top.contributors/jesyspa.html":
            return  ('<a href="http://top.contributors/elssar.html">'
        '<a href="http://top.contributors/kilaws.html">')
        elif url == "http://top.contributors/forbiddenvoid.html":
            return ('<a href="http://top.contributors/charlzz.html">'
        '<a href="http://top.contributors/johang.html">'
        '<a href="http://top.contributors/graemeblake.html">')
        elif url == "http://top.contributors/kilaws.html":
            return ('<a href="http://top.contributors/tomvandenbosch.html">'
        '<a href="http://top.contributors/mathprof.html">')
        elif url == "http://top.contributors/graemeblake.html":
            return ('<a href="http://top.contributors/dreyescat.html">'
        '<a href="http://top.contributors/angel.html">')
        elif url == "A1":
            return  '<a href="B1"> <a href="C1">  '
        elif url == "B1":
            return  '<a href="E1">'
        elif url == "C1":
            return '<a href="D1">'
        elif url == "D1":
            return '<a href="E1"> '
        elif url == "E1":
            return '<a href="F1"> '
    except:
        return ""
    return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

'''
def crawl_web(seed,max_pages):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled and len(crawled) < max_pages:
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
'''

'''
def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    depth_count = 0;
    while tocrawl:
        if depth_count > max_depth:
            break;
        else:
            temp = [];
            while tocrawl:
                temp.append(tocrawl.pop());
            for page in temp:
                if page not in crawled:
                    union(tocrawl, get_all_links(get_page(page)))
                    crawled.append(page);
            depth_count = depth_count + 1;
    return crawled;
'''
def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    depth_count = 0;
    while tocrawl and depth_count <= max_depth:
        temp = tocrawl;
        tocrawl = [];
        for page in temp:
            if page not in crawled:
                union(tocrawl, get_all_links(get_page(page)))
                crawled.append(page);
        depth_count = depth_count + 1;
    return crawled;

'''
def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    next_depth = []
    depth = 0
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            union(next_depth, get_all_links(get_page(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
    return crawled
'''
correct = [[1,2,3],
           [2,3,1],
           [3,1,2]]

incorrect = [[1,2,3,4],
             [2,3,1,3],
             [3,1,2,3],
             [4,4,4,4]]

incorrect2 = [[1,2,3,4],
             [2,3,1,4],
             [4,1,2,3],
             [3,4,1,2]]

incorrect3 = [[1,2,3,4,5],
              [2,3,1,5,6],
              [4,5,2,1,3],
              [3,4,5,2,1],
              [5,6,4,3,2]]

incorrect4 = [['a','b','c'],
              ['b','c','a'],
              ['c','a','b']]

incorrect5 = [ [1, 1.5],
               [1.5, 1]]

def check_sudoku (square):
    isgood = True;
    whole_number = [1, 2, 3, 4, 5, 6, 7, 9];
#    for row in square:
#        index = 0;
#        while (index + 1) < len(row):
#            if row[index] in row[(index + 1):]:
#                ok = ok and False;
#            index = index + 1;
            
#    column_i = 0; 
#    row_i = 0;
#    while (row_i + 1) < len(square):
#        print (square[row_i][column_i]);
#        if square[row_i][column_i] not in whole_number:
#            print ('check ');
#            isgood = False;
#            break;
#        # validate row (except last row)
#        index = 0;
#        while (index + 1) < len(square[row_i]):
#            if square[row_i][index] in square[row_i][(index + 1):]:
#                isgood = isgood and False;
#            index = index + 1;
#        # validate column
#        if square[row_i][column_i] == square[row_i + 1][column_i]:
#            isgood = isgood and False;
#        
#        column_i = column_i + 1;
#        row_i = row_i + 1;
    
    row = 0; 
    col = 0;
    while row < len(square):
        if square[row][col] not in whole_number:
            isgood = False;
        elif square[row][col] > len(square[row]):
            isgood = False;
        else:
            # validate row
            index = 0;
            while (index + 1) < len(square[row]):
                if square[row][index] in square[row][(index + 1):]:
                    isgood = isgood and False;
                index = index + 1;
            # validate column
            if (row + 1) < len(square) and square[row][col] == square[row + 1][col]:
                isgood = isgood and False;
        
        col = col + 1;
        if col == len(square[row]):
            col = 0;
            row = row + 1;
        
#    print (ok);
#    if ok:
#        print ('Check column '), (ok);
#        for row in square:
#            i = 0;
#            j = 0;
#            while j < len(square):
#                if row[j][i] == row[j+1][i]:
#                    ok = ok and False;
#                j = j + 1;
#                i = i + 1;

    return isgood;


index = []

def add_to_index1 (index,keyword,url):
    checked_keywords = [];
    if index:
        for e in index:
            if keyword not in checked_keywords:
                if keyword == e[0]:
                    e[1].append(url);
                else:
                    index_row = [];
                    index_urls = [];
                    index_urls.append(url);
                    index_row.append(keyword);
                    index_row.append(index_urls);
                    index.append(index_row);
                checked_keywords.append(keyword);
    else:
        index_row = [];
        index_urls = [];
        index_urls.append(url);
        index_row.append(keyword);
        index_row.append(index_urls);
        index.append(index_row);
        
def add_to_index2 (index, keyword, url):
    keywordnotfound = True;
    for entry in index:
        if entry[0] == keyword:
            keywordnotfound = False;
            if url not in entry[1]:
                entry[1].append(url);
            return;
    # not found, add new keyword to index
    if keywordnotfound:
        index.append([keyword, [url]]);
        
def add_to_index (index,keyword,url):
    for entry in index:
        if keyword == entry[0]:
            for e in entry[1]:
                if url == e[0]:
                    return;
            entry[1].append([url, 0]);
            return;
    # not found, add new keyword to index
    index.append([keyword, [[url, 0]]]);
    
def lookup (index,keyword):
    for e in index:
        if keyword == e[0]:
            return e[1];
    return [];

def add_page_to_index(index,url,content):
    keywords = content.split();
    for keyword in keywords:
        add_to_index(index, keyword, url);

def crawl_web_1(seed):
    tocrawl = [seed];
    crawled = [];
    index = [];
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page);
            add_page_to_index (index, page, content);
            union(tocrawl, get_all_links(content));
            crawled.append(page)
    return crawled

def add_to_index_2(index,keyword,url):
    if keyword in index:
        index[keyword].append(url);
    else:
        index[keyword] = [url];

def add_page_to_index_2(index,url,content):
    keywords = content.split();
    for keyword in keywords:
        add_to_index_2(index, keyword, url);

def crawl_web_2(seed):
    tocrawl = [seed];
    crawled = [];
    index = {};
    graph = {};
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page);
            add_page_to_index_2(index, page, content);
            outlink = get_all_links(content);
            
            union(tocrawl, outlink);
            crawled.append(page)
    return index, graph;

def get_next_string (string, delim):
    start_pos = string.find(delim);
    if start_pos == -1:
        return string, None;
    return string[0:start_pos], start_pos;

def split_string_using_delimiter (string, delim):
    result = [];
    while True:
        f, pos = get_next_string (string, delim);
        if pos != None:
            if len(f) > 0:
                result.append(f);
            string = string[pos + 1:];
        else:
            if len(f) > 0:
                result.append(f);
            break;
    return result;

def split_all_strings (strings, delim):
    result = [];
    for string in strings:
        result += split_string_using_delimiter (string, delim);
    return result;
         

def split_string1 (source,splitlist):
    delimiters = [];
    result = [source];
    
    i = 0;
    while i < len(splitlist):
        delimiters.append(splitlist[i]);
        i = i + 1;
        
    for delimiter in delimiters:
        result = split_all_strings (result, delimiter);
            
    return result;

def split_string (source,splitlist):
    result = [];
    tosplit = True;
    for char in source:
        if char in splitlist:
            tosplit = True;
        else:
            if tosplit:
                tosplit = False;
                result.append(char);
            else:
                result[-1] = result[-1] + char;
    return result;
      
'''    
def dothis ():
    string = '12asdad2131234asd';
    string.__len__
    i = 0;
    while string[i:i+1]:
        print string[i:i+1];
        i = i + 1;
'''
def dothis ():
    string = 'asdasdasfjhqgqweqe qwe';
    r = [];
    for s in string:
        r.append(s);
    print (r);


def record_user_click(index,keyword,url):
    url_list = lookup(index, keyword);
    if url_list:
        for url_entry in url_list:
            if url_entry[0] == url:
                url_entry[1] = url_entry[1] + 1;
        
        
def hash_string(keyword,buckets):
    mod = 0;
    for w in keyword:
        mod = (mod + ord(w)) % buckets;
    return mod;

def test_hash_function (func, keywords, size):
    results = [0] * size;
    keys_used = [];
    for w in keywords:
        if w not in keys_used:
            hv = func(keywords, size);
            results[hv] += 1;
            keys_used.append(w);
    return results;

def make_hashtable1(nbuckets):
    hashtable = [];
    i = 0;
    while i < nbuckets:
        hashtable.append([]);
        i = i + 1;
    return hashtable;

def make_hashtable(nbuckets):
    hashtable = [];
    for unused in range(0, nbuckets):
        hashtable.append([]);
    return hashtable;

def hashtable_get_bucket(htable,keyword):
    return htable[hash_string(keyword, len(htable))];

def hashtable_add(htable,key,value):
    bucket = hashtable_get_bucket(htable, key);
    bucket.append([key, value]);
    return htable;

def hastable_find(htable,key):
    bucket = hashtable_get_bucket(htable, key);
    for entry in bucket:
        if key == entry[0]:
            return entry;
    return None;

def hashtable_lookup(htable,key):
    entry = hastable_find(htable,key);
    if entry:
        return entry[1];
    else:
        return None;
'''
def hashtable_update(htable,key,value):
    bucket = hashtable_get_bucket(htable, key);
    for entry in bucket:
        if key == entry[0]:
            entry[1] = value;
            return htable;
    return hashtable_add(htable, key, value);
'''
def hashtable_update(htable,key,value):
    entry = hastable_find(htable,key);
    if entry:
        entry[1] = value;
        return htable;
    else:
        return hashtable_add(htable, key, value);
   
population = {"Shanghai" : 17.8, "Istanbul" : 13.3, "Karachi" : 13.0, "Mumbai" : 12.5};

def lookup_2(index,keyword):
    if keyword in index:
        return index[keyword];
    else:
        return None;
    

def get_page_url(url):
    try:
        #import urllib.request;
        #return urllib.request.urlopen(url).read();
        import urllib;
        return urllib.urlopen(url).read();
    except:
        # return an empty sting
        return "";
    
def get_links_using_lib(page):
    from bs4 import BeautifulSoup;
    soup = BeautifulSoup(page);
    count, links = 0, [];
    for link in soup.find_all('a'):
        print ("{urllink}\n".format(urllink=link));
        li = link.get('href');
        #print (type(li));
        if li and type(li) == unicode:
            links.append(li.encode("utf-8")); #.encode("utf-8")
        count = count + 1;
    print ("Number of URL links is {count}".format(count=count));
    return links;


pp = [[1,2,3,4,5], 
[2,3,1,5,6], 
[4,5,2,1,3], 
[3,4,5,2,1], 
[5,6,4,3,2]];

[[1,2,3,4], 
[2,4,1,3], 
[3,1,4,2], 
[4,3,2,1]]

p = [[1], [2, 1], [3, 2, 1]];
h = [7,8,9,0];
h += [1, 2, 3];

sss = ";sf;fjkl;jk+f;";
ssss = ' asd ad ad ad ';
sssss = ['ad;bbdg', ';sf;fjkl;jk+f;'];
mmm = ['This', ['http://free.org', 0], ['http://free.org', 0], ['http://free.org', 0]];
#print (product_list(p));
#print (greatest(p));
#print (total_enrollment(usa_univs));
#print (crawl_web('A1', 50));
#print (p[2:][0][3]);
#print (h);
#print (check_sudoku(p));
#add_to_index(index,'udacity','http://udacity.com');
#add_to_index(index,'computing','http://acm.org');
#add_to_index(index,'udacity','http://npr.org');
#add_to_index(index,'udacity','http://npr.org');
#add_to_index(index,'udacity','http://npr.org');
#add_page_to_index(index,'http://free.org',"This This This");
#add_page_to_index(index,'http://msn.org',"This This This");
#record_user_click(index,'This', 'http://free.org');
#print (lookup(index, 'This'));
#record_user_click(index, "This", "http://msn.org");
#print (lookup(index, 'This'));
#print (dothis());
#print (split_string_using_delimiter (sss, ';'));
#print (len(sss));
#print (ssss.split('a'));
#print (split_all_strings (sssss, ';'));
#print (split_string1("First Name,Last Name,Street Address,City,State,Zip Code",","));
#print (sssss[-1]);
#print (eval("3*90"));
#print (ord(5));
#print (hash_string ('searchwithpeter.info', 73));
#hashtable = [[['Francis', 13], ['Ellis', 11]], [], [['Bill', 17], ['Zoe', 14]], [['Coach', 4]], [['Louis', 29], ['Rochelle', 4], ['Nick', 2]]];
#print (hashtable_get_bucket(hashtable, "Zoe"));
'''
table = make_hashtable(5)
hashtable_add(table,'Bill', 17)
hashtable_add(table,'Coach', 4)
hashtable_add(table,'Ellis', 11)
hashtable_add(table,'Francis', 13)
hashtable_add(table,'Louis', 29)
hashtable_add(table,'Nick', 2)
hashtable_add(table,'Rochelle', 4)
hashtable_add(table,'Zoe', 14)
print (table);
'''
'''
table = [[['Ellis', 11], ['Francis', 13]], [], [['Bill', 17], ['Zoe', 14]], [['Coach', 4]], [['Louis', 29], ['Nick', 2], ['Rochelle', 4]]]
hashtable_update(table, 'Bill', 42)
hashtable_update(table, 'Rochelle', 94)
hashtable_update(table, 'Zed', 68)
print (table);
'''
'''
table = make_hashtable(10);
hashtable_update(table, 'Python', 'Monty');
hashtable_update(table, 'CLU', 'Barbara Liskov');
hashtable_update(table, 'JavaScript', 'Brendan Eich');
print (hashtable_lookup(table, 'Python'));
hashtable_update(table, 'Python', 'Guido van Rossum');
print (hashtable_lookup(table, 'Python'));
'''
#mmm = {"a" : 123, "a": 456, "a": 789};
#print (mmm.get('a'));

htmPageCode = get_page_url("http://www.udacity.com/cs101x/index.html");
#print (get_links_using_lib(htmPageCode));
