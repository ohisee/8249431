# -*- coding: UTF-8 -*-
'''
'''

def escape_html_cgi(s):
    import cgi;
    return cgi.escape(s, quote=True);

#Escape at using jinja2 - autoescape = True
def applyRot13(s, rotval=13):
    alpha_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                   'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    alpha_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                   'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
                   'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    s_list = list(s);
    for i in range(0, len(s_list)):
        if (s_list[i] in alpha_upper):
            index = (alpha_upper.index(s_list[i]) + rotval) % len(alpha_upper);
            s_list[i] = alpha_upper[index];
        elif (s_list[i] in alpha_lower):
            index = (alpha_lower.index(s_list[i]) + rotval) % len(alpha_lower);
            s_list[i] = alpha_lower[index];
    return ''.join(s_list);