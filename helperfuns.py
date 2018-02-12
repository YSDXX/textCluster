#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 14:19:21 2018

@author: everitt257
"""

def readbyline(file):
    return [line.rstrip() for line in open(file)]




if __name__=="__main__":
    file = "./chineseStopwords.txt"
    stpwrdlist = readbyline(file)