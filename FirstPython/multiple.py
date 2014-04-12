#!/usr/bin/python
# -*- coding: utf-8 -*-

def multiply(a, b):
    if a == 0:
        return a;
    if a == 1 or a == -1:
        return a * b;
    else:
        if a % 2 != 0:
            return b + multiply(a/2, b*2);
        else:
            return multiply(a/2, b*2);


if __name__ == "__main__":
    print (multiply(12, 873));
