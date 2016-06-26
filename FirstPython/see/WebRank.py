'''
url: [list of pages url links to] 

'''

def crawl_web(seed): # returns index, graph of outlinks
    tocrawl = [seed];
    crawled = [];
    graph = {};  # <url>:[list of pages it links to]
    index = {};
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page);
            add_page_to_index(index, page, content);
            outlinks = get_all_links(content);
            #Build link graph
            graph[page] = outlinks;
            union(tocrawl, outlinks);
            crawled.append(page);
    return index, graph;

#crawl web function using sets
def crawl_web_using_sets(seed):
    tocrawl = set([seed]);  # this should be a set
    crawled = set([]);      # this should be a set
    graph = {};
    index = {} ;
    while tocrawl: 
        page = tocrawl.pop();
        if page not in crawled:
            content = get_page(page);
            add_page_to_index(index, page, content);
            outlinks = get_all_links(content);
            graph[page] = outlinks;
            tocrawl.update(outlinks);
            crawled.add(page);
    return index, graph;

cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""", 
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""", 
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""", 
}

def get_page(url):
    if url in cache:
        return cache[url]
    else:
        return None
    
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def compute_ranks(graph):
    d = 0.8         # damping factor
    numloops = 10;
    
    ranks = {};
    npages = len(graph);
    for page in graph:
        ranks[page] = 1.0 / npages;
        
    for i in range(0, numloops):
        newranks = {};
        for page in graph:
            newrank = (1 - d) / npages;
            #core - rank sum of in link(s)
            for p in graph:
                if page in graph[p]:
                    outlink = len(graph[p]);
                    if outlink == 0:
                        outlink = 1;
                    newrank = newrank + d * (ranks[p] / outlink);
            
            newranks[page] = newrank;
        ranks = newranks;
    return ranks;

def is_node_reciprocal_link(graph, k, node, page):
    if k > 0:
        link_nodes = [];
        if page in graph:
            link_nodes = link_nodes + graph[page];
        count = 1;
        found = False;
        while count <= k and not found:
            if node not in link_nodes:
                temp_link_nodes, link_nodes = link_nodes, [];
                for t_node in temp_link_nodes:
                    if t_node in graph:
                        link_nodes = link_nodes + graph[t_node];
                count = count + 1;
            else:
                found = True;
        if found:
            if k >= count:
                return True;
        return False;
    else:
        return (node == page);
                

def compute_ranks_reciprocal(graph, k):
    d = 0.8; # damping factor
    numloops = 10;
    ranks = {};
    npages = len(graph);
    for page in graph:
        ranks[page] = 1.0 / npages;
    for i in range(0, numloops):
        newranks = {};
        for page in graph:
            newrank = (1 - d) / npages;
            for node in graph:
                if page in graph[node]:
                    if not is_node_reciprocal_link(graph, k, node, page):
                        newrank = newrank + d * (ranks[node]/len(graph[node]));
            newranks[page] = newrank;
        ranks = newranks;
    return ranks;

def lucky_search(index, ranks, keyword):
    urls = lookup(index, keyword);
    if urls:
        rank = urls[0];
        for url in urls:
            if ranks[url] > ranks[rank]:
                rank = url;
        return rank;
    else:
        return None;

#Use quick sort - in descending order
def sort_ranks_desc(rankslist):
    if len(rankslist) <= 1:
        return rankslist;
    pivot = rankslist[0];
    rankslist = rankslist[1:];
    lessorequal = [];
    greater = [];
    result = [];
    for e in rankslist:
        if e[1] <= pivot[1]:
            lessorequal.append(e);
        else:
            greater.append(e);
    result = result + sort_ranks_desc(greater);
    result.append(pivot);
    result = result + sort_ranks_desc(lessorequal);
    return result;

def ordered_search(index, ranks, keyword):
    urls = lookup(index, keyword);
    if urls:
#        rankslist = [];
#        for url in urls:
#            if url in ranks:
#                rankslist.append([url, ranks[url]]);
#        rankslist = sort_ranks_desc (rankslist);
#        result = [];
#        for e in rankslist:
#            result.append(e[0]);
#        return result;
        return qucik_sort_ranks_desc(urls, ranks);
    else:
        return None;

def qucik_sort_ranks_desc (rankslist, ranks):
    if not rankslist or len(rankslist) <= 1:
        return rankslist;
    pivot = ranks[rankslist[0]];
    lessorequal = [];
    greater = [];
    result = [];
    for e in rankslist[1:]:
        if ranks[e] <= pivot:
            lessorequal.append(e);
        else:
            greater.append(e);
    result = result + qucik_sort_ranks_desc(greater, ranks);
    result.append(rankslist[0]);
    result = result + qucik_sort_ranks_desc(lessorequal, ranks);
    return result;
    


index , graph = crawl_web_using_sets('http://udacity.com/cs101x/urank/index.html');
ranks = compute_ranks(graph);

#if 'http://udacity.com/cs101x/urank/index.html' in graph:
#    print (graph['http://udacity.com/cs101x/urank/index.html'])
#>>> ['http://udacity.com/cs101x/urank/hummus.html',
#'http://udacity.com/cs101x/urank/arsenic.html',
#'http://udacity.com/cs101x/urank/kathleen.html',
#'http://udacity.com/cs101x/urank/nickel.html',
#'http://udacity.com/cs101x/urank/zinc.html']
#print (graph);
#print (compute_ranks(graph));
#print (index);
#print (lucky_search(index, ranks, 'Hummus'));
#print (ranks);
#print (lookup(index, 'tablesppons'));

#sort = [4, 2, 3, 7, 1, 9, 11, 10, 5];
#print (sort_ranks(sort));

#print (ordered_search(index, ranks, 'Hummus'));

#g = {'a': ['b', 'c'], 'b':['a', 'e'], 'c':['d'], 'd':['b']}
#g = {'a': ['a', 'b', 'c'], 'b':['a'], 'c':['d'], 'd':['a']}
#print (is_node_reciprocal_link(g, 2, 'd', 'a'));