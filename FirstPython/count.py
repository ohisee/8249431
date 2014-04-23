#!/usr/bin/python

import math;

def countdown(n):
    y = 0;
    while x > 0:
        x = x - 5;
        y = y + 1;
    print y;

def time_countdown(n):
    steps = math.ceil(n / 5.0) * 2 + 3;
    return steps;

def naive(a, b):
    x = a
    y = b
    z = 0
    while x > 0:
        z = z + y
        x = x - 1
    return z
