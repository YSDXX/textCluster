#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:10:34 2018

@author: everitt257
"""

from sklearn.naive_bayes import MultinomialNB
from importer import importer
from builddict import vectorizer
import numpy as np

class BayesPredict:
    def __init__(self):
        pass
    
    def trainClassifier(self, trainData):
        self.clf1 = MultinomialNB(alpha=0.01).fit(trainData.tqm, trainData.labels1)
        self.clf2 = MultinomialNB(alpha=0.01).fit(trainData.tqm, trainData.labels2)
    
    def predict(self, data):
        self.pdata = data
        self.predicted1 = self.clf1.predict_proba(data.tqm)
        self.predicted2 = self.clf2.predict_proba(data.tqm)
        return self.predicted1, self.predicted2
    
    def printResult(self):
        plabels = self.clf1.classes_[np.argmax(self.predicted1,1)]
        pprobs = np.max(self.predicted1,1)
        truelabels = self.pdata.labels1
        wrongList = []
        fullList = []
        for plabel, pprob, tlabel in zip(plabels, pprobs, truelabels):
            fullList.append("predicted: {}, actual: {}, predicted prob: {}".format(plabel, tlabel, pprob))
            if plabel != tlabel:
                wrongList.append("predicted: {}, actual: {}, predicted prob: {},".format(plabel, tlabel, pprob))
        
        print("The average accuracy is: {}".format((len(fullList) - len(wrongList))/len(fullList)))
        
        return fullList, wrongList

if __name__ == "__main__":
    
    fileStplist = "./chineseStopwords.txt"
    fileName = "1月1日-12月17日上报网公司周报工单详情.xlsx"
    
    a1 = importer(fileName)
    a1.process()
    
    b2 = vectorizer(fileStplist)
    b2.process()
    
    c3 = BayesPredict()
    c3.trainClassifier(b2)
    p1, p2 = c3.predict(b2)
    fullList, wrongList = c3.printResult()
