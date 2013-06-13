# -*- coding: UTF-8 -*-

s = 'jasdnncasdsadsafff';
t = 'FF';
i = 1;
#print (s.find(t));
#print (s.find(t, i));
#print (s[i:].find(t)+i);
#print (s[i:].find(t[i:]));
#print (s[i:].find(t));

page = ('<div id="top_bin"><div id="top_content" class="width960">''<div class="udacity float-left"><a href="http://udacity.com">');
search_string = '<a href=';
start_link  = page.find(search_string);
href = page[start_link:];
href_start = href.find('"') + 1;
href_end = href.find('">');
url = href[href_start:href_end];
#print (url);

#print (24*7*7);

x = 7;
a = 0;
a, x = x, a
#print (a);
a, x = x, a
#print (a);
#print (x);

speed_of_light = 299800000. # meters per second
nano_per_sec = 1000000000. # 1 billion
nanodistance = speed_of_light / nano_per_sec;
#print (nanodistance);

s = 'udacity'
t = 'bodacious'
#print (s[0:1] + t[2:]);

text = "all zip files are zipped";
search_string = 'zip';
#print (text.find(search_string, text.find(search_string) + search_string.__len__()));

x = 3.4;
x = x + 0.5;
x = str(x);
x = x[:x.find('.')];
#print (x);



def check_sudoku (square):
    isgood = True;
    whole_number = [1, 2, 3, 4, 5, 6, 7, 9];
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
        if (col == len(square[row])):
            col = 0;
            row = row + 1;

    return isgood;
    

courses = {
    'feb2012': { 'cs101': {'name': 'Building a Search Engine',
                           'teacher': 'Dave',
                           'assistant': 'Peter C.'},
                 'cs373': {'name': 'Programming a Robotic Car',
                           'teacher': 'Sebastian',
                           'assistant': 'Andy'}},
    'apr2012': { 'cs101': {'name': 'Building a Search Engine',
                           'teacher': 'Dave',
                           'assistant': 'Sarah'},
                 'cs212': {'name': 'The Design of Computer Programs',
                           'teacher': 'Peter N.',
                           'assistant': 'Andy',
                           'prereq': 'cs101'},
                 'cs253': 
                {'name': 'Web Application Engineering - Building a Blog',
                           'teacher': 'Steve',
                           'prereq': 'cs101'},
                 'cs262': 
                {'name': 'Programming Languages - Building a Web Browser',
                           'teacher': 'Wes',
                           'assistant': 'Peter C.',
                           'prereq': 'cs101'},
                 'cs373': {'name': 'Programming a Robotic Car',
                           'teacher': 'Sebastian'},
                 'cs387': {'name': 'Applied Cryptography',
                           'teacher': 'Dave'}},
    'jan2044': { 'cs001': {'name': 'Building a Quantum Holodeck',
                           'teacher': 'Dorina'},
                 'cs003': {'name': 'Programming a Robotic Robotics Teacher',
                           'teacher': 'Jasper'},
                     }
    }

def courses_offered(courses, hexamester):
    res = []
    for c in courses[hexamester]:
        res.append(c)
    return res

def is_offered(courses, course, hexamester):
    return course in courses[hexamester];

def when_offered(courses,course):
    result = [];
    for key in courses:
        if course in courses[key]:
            result.append(key);
    return result;

def involved(courses, person):
    involved_hexamester = {};
    for hexamester in courses:
        involved_courses = [];
        for course in courses[hexamester]:
            if "teacher" in courses[hexamester][course] and person == courses[hexamester][course]["teacher"]:
                involved_courses.append(course);
            if "assistant" in courses[hexamester][course] and person == courses[hexamester][course]["assistant"]:
                involved_courses.append(course);
        if len(involved_courses) > 0:
            involved_hexamester[hexamester] = involved_courses
    return involved_hexamester;

def involved1(courses, person):
    for hexamester in courses:
        for course in courses[hexamester]:
            if "teacher" in courses[hexamester][course]:
                print (courses[hexamester][course]["teacher"]);


def factorial(n):
    if n == 0:
        return 1;
    else:
        return n * factorial(n - 1);
    
def is_palindrome(s):
    print (s);
    if s == "":
        return True;
    else:
        if (s[0] != s[-1]):
            return False;
        else:
            return is_palindrome(s[1:-1]);
        
        
def fibonacci(n):
    if n == 0:
        return 0;
    elif n == 1:
        return 1;
    else:
        return fibonacci(n - 1) + fibonacci(n - 2);
    
def fibonacci_using_loop(n):
    f0 = 0;
    f1 = 1;
    i = 0;
    while (i < n):
        f0, f1 = f1, f0 + f1;
        i = i + 1;
    return f0;


def rabbits(n):
    if n == 1 or n == 2:
        return 1;
    if n >= 3 and n <= 5:
        return rabbits(n - 1) + rabbits(n - 2);
    if n > 5:
        return rabbits(n - 1) + rabbits(n - 2) - rabbits(n - 5);
    

def hexes_to_udaciousness(n, spread, target):
    if n >= target:
        return 0;
    else:
        return 1 + hexes_to_udaciousness(n + (n * spread), spread, target);
    
def is_list(p):
    return isinstance(p, list);

def deep_count(p):
    if is_list(p):
        count = 0;
        for e in p:
            count = count + 1 + deep_count(e);
        return count;
    else:
        return 0;
    
    
ada_family = { 'Judith Blunt-Lytton': ['Anne Isabella Blunt', 'Wilfrid Scawen Blunt'],
              'Ada King-Milbanke': ['Ralph King-Milbanke', 'Fanny Heriot'],
              'Ralph King-Milbanke': ['Augusta Ada King', 'William King-Noel'],
              'Anne Isabella Blunt': ['Augusta Ada King', 'William King-Noel'],
              'Byron King-Noel': ['Augusta Ada King', 'William King-Noel'],
              'Augusta Ada King': ['Anne Isabella Milbanke', 'George Gordon Byron'],
              'George Gordon Byron': ['Catherine Gordon', 'Captain John Byron'],
              'John Byron': ['Vice-Admiral John Byron', 'Sophia Trevannion'] }

def ancestors(genealogy, person):
    ancs = [];
    tosearch = [];
    if person in genealogy:
        ancs += genealogy[person];
        tosearch += genealogy[person]; 
        while tosearch:
            p = tosearch.pop();
            if p in genealogy:
                ancs += genealogy[p];
                tosearch += genealogy[p];
    return ancs;

def pick_one(boolean, a, b):
    if boolean:
        return a;
    else:
        return b;

def triangular_1(n):
    result = 0;
    for i in range (0, n + 1):
        result = result + i;
    return result;

def triangular(n):
    if n == 0:
        return n;
    else:
        return n + triangular(n - 1);
    
def triangle(n):
    trilist = [];
    if n > 0:
        for i in range (0, n):
            result = [1];
            if i > 0:
                f0 = 0;
                pre = 0;
                toadd = False;
                for e in trilist[i - 1]:
                    if toadd:
                        f0, pre = pre + e, e;
                        result.append(f0);
                    else:
                        toadd, pre = True, e;
                result.append(1);
            trilist.append(result);
    return trilist;

def proc2(input_list):
    sum = 0
    while len(input_list) > 0:
        sum = sum + input_list[0]   # Assume input_list[0] is constant time
        input_list = input_list[1:]  # Assume input_list[1:] is constant time
    return sum

def remove_tags(htmlString):
    words = [];
    if len(htmlString) > 0:
        toskip = False;
        tosplit = True;
        for char in htmlString:
            if char == "<":
                toskip = True;
            elif char == ">":
                toskip = False;
                tosplit = True;
            else:
                if not toskip:
                    if char == " " or char == "\n":
                        tosplit = True;
                    else:
                        if tosplit:
                            tosplit = False;
                            words.append(char);
                        else:
                            words[-1] = words[-1] + char;
    return words;

english = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 
6:"June", 7:"July", 8:"August", 9:"September",10:"October", 
11:"November", 12:"December"}

swedish = {1:"januari", 2:"februari", 3:"mars", 4:"april", 5:"maj", 
6:"juni", 7:"juli", 8:"augusti", 9:"september",10:"oktober", 
11:"november", 12:"december"}

def date_converter(calender, dateString):
    firstslash = dateString.find("/");
    secondslash = dateString.find("/", firstslash + 1);
    month = dateString[0:firstslash];
    date = dateString[firstslash + 1:secondslash];
    year = dateString[secondslash + 1:];
    return (date + " " + calender[int(month)] + " " + year);

def make_converter(match, replacement):
    return [match, replacement];

def apply_converter(converter, string):
    while string.find (converter[0]) != -1:
        startpos = string.find(converter[0]);
        string = string[0:startpos] + converter[1] + string[startpos + len(converter[0]):]
    return string;

def apply_converter_1(converter, string):
    previous = None;
    while previous != string:
        previous = string;
        startpos = string.find(converter[0]);
        if startpos != -1:
            string = string[0:startpos] + converter[1] + string[startpos + len(converter[0]):]
    return string;

def longest_repetition(repetition):
    if repetition:
        cache = {};
        index, key = 0, 0;
        prev = repetition[0];
        cache[key] = 0;
        for e in repetition:
            if prev != e:
                key = index;
                cache[key] = 1;
            else:
                cache[key] = cache[key] + 1;
            prev = e;
            index = index + 1;
            
        occurance = 0;
        for entry in cache:
            rep = cache[entry];
            if cache[entry] > occurance:
                occurance = rep;
                index = entry;
                
        return repetition[index];
    return None;

#print (longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1]));

def deep_reverse(input_list):
    result = [];
    v = -1;
    for i in range(0, len(input_list)):
        index = i + v;
        v = v - 2;
        e = input_list[index];
        if is_list(e):
            t_result = deep_reverse(e);
            result.append(t_result);
        else:
            result.append(e);
    return result;

def deep_reverse_1(input_list):
    if is_list(input_list):
        result = [];
        v = -1;
        for i in range(0, len(input_list)):
            index = i + v;
            v = v - 2;
            result.append(deep_reverse_1(input_list[index]));
        return result;
    else:
        return input_list;


def stirling(n, k):
    if n < 0 or k < 0:
        return 0;
    if n == k or k == 1:
        return 1;
    if n < k:
        return 0;
    return k * stirling(n - 1, k) + stirling(n - 1, k - 1);


def bell(n):
    bellsum = 0;
    for k in range (1, n + 1):
        bellsum = bellsum + stirling(n, k);
    return bellsum;

#print (stirling(5,2));
#print (bell(15));

'''
print (set(set([1, 2, 3])));
print (hash('ooo'));
print (('a', 'b'));
print (set([set]));
print (type(2));

s = set([1, 2, 3]);
ss = set([7, 2, 1]);
print (dir(s));
s.update(ss);
print (s);

sss = set([]);
if sss:
    print ("set");
else:
    print ("not set");
'''

def card_ranks_1(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = [r for r,s in cards]
    cards = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14};
    for i in range(0, len(ranks)):
        if ranks[i] in cards:
            ranks[i] = cards[ranks[i]];
        else:
            ranks[i] = int(ranks[i]);
    ranks.sort(reverse=True)
    return ranks

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    ranks = ["--23456789TJQKA".index(r) for r,s in cards]
    ranks.sort(reverse=True)
    return ranks

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    # Your code here.
#    i = ranks[0] - 1; 
#    stra = True;
#    for r in ranks[1:]:
#        if r == i:
#            i = i - 1;
#        else:
#            stra = False;
#            break;
#    return stra;
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5;
            
def flush(hand):
    "Return True if all the cards have the same suit."
    # Your code here.
    ranks = [s for r,s in hand];
#    suit = True;
#    t = ranks[0];
#    for r in ranks[1:]:
#        if t != r:
#            suit = False;
#            break;
#    return suit;
    return len(set(ranks)) == 1;
    
def test():
    "Test cases for the functions in poker program."
    sf = "6C 7C 8C 9C TC".split()
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    assert flush(sf) == True
    assert flush(fk) == False
    return 'tests pass'

def nextDay(year, month, day):
    """
    Returns the year, month, day of the next day.
    Simple version: assume every month has 30 days.
    """
    # YOUR CODE HERE
    '''
    if day >= 30:
        day, month = 1, month + 1;
        if month >= 12:
            month, year = 1, year + 1;
    else:
        day = day + 1;
    return year, month, day;
    '''
    if day < daysInMonth(year, month):
        return year, month, day + 1;
    else:
        if month == 12:
            return year + 1, 1, 1;
        else:
            return year, month + 1, 1;
        
def isBefore (year1, month1, day1, year2, month2, day2):
    result = False;
    if year1 < year2:
        result = True;
    else:
        if (year1 == year2) and (month1 < month2):
            result = True;
        else:
            if (year1 == year2) and (month1 == month2) and (day1 < day2):
                result = True;
    return result;

def daysInMonth (year, month):
    days = [(31, 31), (28, 29), (31, 31), (30, 30), 
            (31, 31), (30, 30), (31, 31), (31, 31), 
            (30, 30), (31, 31), (30, 30), (31, 31)];
    if 13 > month and 0 < month:
        if isLeapYear(year):
            return days[month - 1][1];
        else:
            return days[month - 1][0];
    else:
        return 0;

def isLeapYear (year):    
    return (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0));  

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    """Returns the number of days between year1/month1/day1
       and year2/month2/day2. Assumes inputs are valid dates
       in Gergorian calendar, and the first date is not after
       the second."""
    
    assert not isBefore(year2, month2, day2, year1, month1, day1);
    # YOUR CODE HERE!
    days = 0;
    while isBefore(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay (year1, month1, day1);
        days = days + 1;
    return days;

def testDays():
    test_cases = [((2012,9,30,2012,10,30),30), 
                  ((2012,1,1,2013,1,1),360),
                  ((2012,9,1,2012,9,4),3),
                  ((2013,1,1,1999,12,31), "AssertionError")]
    
    for (args, answer) in test_cases:
        try:
            result = daysBetweenDates(*args)
            if result != answer:
                print ("Test with data:", args, "failed")
            else:
                print ("Test case passed!")
        except AssertionError:
            if answer == "AssertionError":
                print ("Nice job! Test case {0} correctly raises AssertionError!\n".format(args))
            else:
                print ("Check your work! Test case {0} should not raise AssertionError!\n".format(args))  
                
                
def my_append (element, lst=[]):
    lst.append(element);
    return lst;  

def another_append(element, lst=None):
    if lst is None:
        lst = [];
    lst.append(element);
    return lst;


# Use quick sort
def simple_quick_sort(rankslist):
    # base case
    if not rankslist or len(rankslist) <= 1:
        return rankslist;
    pivot = rankslist[0];
    lessorequal = [];
    greater = [];
    result = [];
    for e in rankslist[1:]:
        if e <= pivot:
            lessorequal.append(e);
        else:
            greater.append(e);
    result = result + simple_quick_sort(lessorequal);
    result.append(pivot);
    result = result + simple_quick_sort(greater);
    return result;

def simple_merge_sort(rankslist):
    if not rankslist or len(rankslist) <= 1:
        return rankslist;
    midIndex = len(rankslist) // 2;
    left = simple_merge_sort (rankslist[0:midIndex]);
    right = simple_merge_sort (rankslist[midIndex:]);
    return merge(left, right);

# Merge two lists in order
#tempList = inputListA + inputListB;
#result = [];
#while tempList:
#result.append(tempList.pop(tempList.index(min(tempList))));
#return result;
#tempList.sort();
#return tempList;
def merge(inputListL, inputListR):
    i, j, result = 0, 0, [];
    while i < len(inputListL) and j < len(inputListR):
        if inputListL[i] < inputListR[j]:
            result.append(inputListL[i]);
            i = i + 1;
        else:
            result.append(inputListR[j]);
            j = j + 1;
    if i < len(inputListL):
        result = result + inputListL[i:];
    if j < len(inputListR):
        result = result + inputListR[j:];
    return result;


#print (courses_offered(courses, "jan2044"));
#print (is_offered(courses, 'cs001', "jan2044"));
#print (when_offered(courses, 'cs101'));
#print (when_offered(courses, 'bio893'));
#print (involved(courses, 'Dave'));
#print (involved1(courses, "Dave"));
#print (factorial (0));
#print (is_palindrome("adaa"));
#ss = "asdcv";
#print (ss[1:-1]);
#print (fibonacci (15));
#print (fibonacci_using_loop(8));
#print (123, 123);
#print ("123123123", 1);
#sss = "";
#for i in range(1, 12):
#    sss = sss + str (rabbits(i)) + " "
#print (sss);
#print (hexes_to_udaciousness(50000, 2, 150000));
#print (isinstance ([], list));
#print (deep_count([[[[[[[[1, 2, 3]]]]]]]]));
#print (ancestors(ada_family, 'Judith Blunt-Lytton'));
#print (triangular(10));
#print (triangle(6));
#print (proc2([1, 2, 3]));
#print (remove_tags('''<h1>Title</h1><p>This is a
#                    <a href="http://www.udacity.com">link</a>.<p>'''));
#print (date_converter(english, '5/11/2012'));
#print (apply_converter(make_converter('aa', 'a'), 'aaaa'));
#p = [1, [2, 3, [4, [5, [6, 7]]]], [8, 9]]
#pp = [1, 2, 3, 4, 5, 6]
#print (deep_reverse(p));
#print (deep_reverse_1(pp));

#rint (pp*2);
#print ("6C 7C 8C 9C TC".split());
#print ( (7, 8, [8, 7, 5]) > (7, 8, [9, 8, 7]));
#print ([x**2 for x in range(1, 10)]);
cards = "6C 7C 8C 9C TC".split();
ranks = [r for r,s in cards];
#print (ranks);
#print (card_ranks(['AC', '3D', '4S', 'KH']));
#print (test());
d = 31 + 31 + 30 + 31 + 30 + 31 + 31 + 28 + 31 + 30 + 31 + 29;
du = (1, 3);
#print (du[1]);
#print (daysBetweenDates(2011, 2, 2, 2011, 2, 3));
'''
x = type
print (type(x) == x);
print (type(12 + 12));
print (type(12 + 12.567));
print (type('qq' + 'bb'));
#print (type('qq' + 33)); # error
print (type([3] + [7]));
#print (type({'a' : 3} + {'b' : 0})); # error
'''
'''
x = 3; print(type(x));
x = 'hello'; print(type(x));
def double(x): return x + x; 
print('asd ',type(x));
x = double; print(type(x));
'''

#from see.Restaurant import Restaurant;
#lunch = Restaurant('asdddddd', 'd', 'w');
#lunch.display();
#print (lunch.is_yummy());

#p = my_append("aabc", my_append('nnnnnnnnn'));
#q = my_append("vvvvvv")

#print (simple_quick_sort(['j', 'c', 'h']));
inputA = [5, 5, 5, 1, 3, 10, 55, 7, 23, 14, 9, 6, 16];
inputB = [11, 17, 8];
midIndex = len(inputA) // 2;
#print (simple_merge_sort(inputB));
#rint (inputA[0:midIndex], inputA[midIndex:]);
#print (midIndex);
#print (type("a"));
#print('jNUEE'.capitalize());

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    if (month and isinstance(month, str)):
        month = month.capitalize();
        if (month in months):
            return month;
    return None;

def valid_day(day):
    if (day and day.isdigit()):
        day = int(day);
        if (day > 0 and day <= 31):
            return day;
    return None;

def valid_year(year):
    if (year and year.isdigit()):
        year = int(year);
        if (year >= 1900 and year <= 2020):
            return year;
    return None;

given_string = "I think %s is a perfectly normal thing to do in public."
def sub1(s):
    return given_string % (s);

given_string2 = "I think %s and %s are perfectly normal things to do in public."
def sub2(s1, s2):
    return given_string2 % (s1, s2);

given_string3 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
def sub_m(name, nickname):
    return given_string3 % {'name' : name, 'nickname' : nickname};

# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
def escape_html(s):
    escape_chars = {'>' : '&gt;', '<' : '&lt;', '"' : '&quot;', '&' : '&amp;'};
    for c, r in escape_chars.iteritems():
        s = s.replace(c, r);
    return s;

def escape_html_cgi(s):
    import cgi;
    return cgi.escape(s, quote=True);

def rot13(s, rotval=13):
    alpha_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    alpha_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    s_list = list(s);
    for i in range(0, len(s_list)):
        if (s_list[i] in alpha_upper):
            index = (alpha_upper.index(s_list[i]) + rotval) % len(alpha_upper);
            s_list[i] = alpha_upper[index];
        elif (s_list[i] in alpha_lower):
            index = (alpha_lower.index(s_list[i]) + rotval) % len(alpha_lower);
            s_list[i] = alpha_lower[index];
    return escape_html_cgi(''.join(s_list));
    
        
def see_function (c, *age):
    print (c);
    if age:
        print(age);
        
def see_two(*a, **kw):
    print (a, kw);

#print valid_day('1')
#print valid_day('15')
#print valid_day('500')
#print (sub_m('wwww', 'dddddd'));
#print (escape_html_cgi('"'));
#print (rot13(""));
#print ("Hello".encode('base64'));

#import os
#print (__file__)
#print (os.path.join(os.path.dirname(__file__), 'NewFile.html'))
#print (os.path.dirname(os.path.realpath(__file__)))
#print (os.path.abspath(os.path.dirname(__file__)))

#see_function('e', 7, 98);
#see_two(a='1234');

alpha = [('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd'), ('E', 'e'), ('F', 'f'), 
         ('G', 'g'), ('H', 'h'), ('I', 'i'), ('J', 'j'), ('K', 'k'), ('L', 'l'),
         ('M', 'm'), ('N', 'n'), ('O', 'o'), ('P', 'p'), ('Q', 'q'), ('R', 'r'),
         ('S', 's'), ('T', 't'), ('U', 'u'), ('V', 'v'), ('W', 'w'), ('X', 'x'),
         ('Y', 'y'), ('Z', 'z')];
alpha_upper = [u for u, l in alpha];
alpha_lower = [l for u, l in alpha];

pa = dict(test='test');
#print (type(pa));
#see_two(**pa);

import hashlib;
x = hashlib.sha256('udacity');
#print (x.hexdigest());
#print ("6C 7C 8C 9C TC".split());

g = [2, 5, 7, 9]
h = [4, 11, 12]

#print (merge(g, h));
import datetime;
#print (datetime.datetime.now());

def real_get_page(url):
    try:
        import urllib;
        return urllib.urlopen(url).read()
    except:
        return ""

# must start http:// as url name
# import urllib2;
# p = urllib2.urlopen('http://www.sfsu.edu');
# print (p.headers.items());

def test_two_p(update):
    if update:
        return 9, 10;
    else:
        return None, None;
    
p1, p2 = test_two_p(False);

print (p1, p2);

if None and None:
    print ('see this');
else:
    print ('see');
    
print ([] + ['abc']);
print (any(['a']));

grammar2 = [
      ("S", ["P", "a" ]),             
      ("S", ["Q", "b" ]),             
      ("P", ["P"]), 
      ("Q", ["c", "d"]),              
      ] 
symbol = 'a';
r = [ ];
for g in grammar2:
    r.append(True if symbol != g[0] else False);
print (r);

for i in range(10):
    for j in range(10):
        if j == 2:
            break;
        print ('j is %d' % j);
    print ('i is %d' % i);