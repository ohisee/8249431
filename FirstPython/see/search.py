'''
Search module

'''

def lookup(index, keyword):
    if keyword in index:
        return index[keyword];
    else:
        return None;

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


