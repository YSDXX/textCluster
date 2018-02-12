#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 12:21:46 2018

@author: everitt257
"""

import jieba
import jieba.analyse
import pickle
from importer import importer
import re
from sklearn.feature_extraction.text import CountVectorizer
from helperfuns import readbyline

class vectorizer:
    def __init__(self, fileStplist=None):
        self.corpus = []
        self.tqm = None
        self.vocab = None
        self.labels = {}
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
        
    def savesegmentedlist(self, name="savedmodel"):
        raw_data = importer.readsavedFile(name)
        self.features = raw_data["features"]
        self.labels["cl1"] = raw_data["labels1"]
        self.labels["cl2"] = raw_data["labels2"]
        jieba.load_userdict("userdict.txt")
        for item in self.features:
            self.segmywords(item)
    
    def tfidfvectorize(self, savename="vectorizersaved"):
        # visit sckit-learn for more details
        try:
            savedV=importer.readsavedFile("vectorizersaved",flag=1)
            vectorizer = CountVectorizer(stop_words=self.stpwrdslist, vocabulary=savedV["vocab"], max_df=0.5)
            self.tqm = vectorizer.fit_transform(self.corpus)
            self.vocab = savedV["vocab"] #keep the old vocab
            
        except:
            print("saved tfidf files not found, building new vocab and tqm")
            vectorizer = CountVectorizer(stop_words=self.stpwrdslist, max_df=0.5)
            self.tqm = vectorizer.fit_transform(self.corpus)
            self.vocab = vectorizer.vocabulary_
        
        finally:
            # saves file, so whenever you have new sentences you can build on top
            # of previous vocab
            print("vectorizing complete")
            self.saveFile(savename)
        
    def saveFile(self, savename="vectorizersaved"):
        """Save vectorizerd result"""
        fileSaved = {"tqm":self.tqm, "vocab":self.vocab}
        pickle.dump(fileSaved, open(savename+".p", "wb"))
        
    def process(self):
        self.savesegmentedlist()
        self.tfidfvectorize()
        
    def topk(self,k=20,fileStplist = "./chineseStopwords.txt", withWeight=True):
        jieba.analyse.set_stop_words(fileStplist)
        content = ".".join(self.features)
        tags = jieba.analyse.extract_tags(content, topK=k, withWeight=withWeight)
#        for tag in tags:
#            print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))
        return tags
    
if __name__ == "__main__":
    
    fileStplist = "./chineseStopwords.txt"
    fileName = "1月1日-12月17日上报网公司周报工单详情.xlsx"
    
    # save segmented list
    a1 = importer(fileName)
    a1.process()
    b1 = vectorizer(fileStplist)
    b1.process()
    
