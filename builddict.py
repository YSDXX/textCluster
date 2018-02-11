#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 12:21:46 2018

@author: everitt257
"""

import jieba
from importer import importer
import re
from sklearn.feature_extraction.text import CountVectorizer
from helperfuns import readbyline

class vectorizer:
    def __init__(self, fileStplist=None):
        self.corpus = []
        self.tqm = None
        self.vocab = None
        if fileStplist:
            self.stpwrdslist = readbyline(fileStplist)
        else:
            self.stpwrdslist = None
        
    def segmywords(self, item):
        item.replace("\r\n","") #remove newline and carriage return
        item.replace(" ","") #remove additonal space
        item = re.sub('\d', '', item) #remove phone numbers
        seg_list = jieba.cut(item,cut_all=False)
        self.corpus.append(" ".join(seg_list))
        
    def savesegmentedlist(self, raw_data):
        features = raw_data["features"]
        for item in features:
            self.segmywords(item)
    
    def tfidfvectorize(self):
        vectorizer = CountVectorizer(stop_words=self.stpwrdslist, max_df=0.5)
        self.tqm = vectorizer.fit_transform(self.corpus)
        self.vocab = vectorizer.vocabulary_
    
            
        
    

if __name__ == "__main__":
    fileStplist = "./chineseStopwords.txt"
    
    # save segmented list
    vectorizer = vectorizer(fileStplist)
    vectorizer.savesegmentedlist(importer.readsavedFile())
    vectorizer.tfidfvectorize()
    
