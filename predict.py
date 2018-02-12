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
        self.predicts = {}
        self.clfs = {}
    
    def trainClassifier(self, trainData):
        self.clfs["cl1"] = MultinomialNB(alpha=0.01).fit(trainData.tqm, trainData.labels["cl1"])
        self.clfs["cl2"] = MultinomialNB(alpha=0.01).fit(trainData.tqm, trainData.labels["cl2"])
    
    def predict(self, data):
        self.pdata = data
        self.predicts["cl1"] = self.clfs["cl1"].predict_proba(data.tqm)
        self.predicts["cl2"] = self.clfs["cl2"].predict_proba(data.tqm)
        return self.predicts
    
    def printResult(self, param="cl1"):
        plabels = self.clfs[param].classes_[np.argmax(self.predicts[param],1)]
        pprobs = np.max(self.predicts[param],1)
        truelabels = self.pdata.labels[param]
        wrongList = []
        fullList = []
        for plabel, pprob, tlabel, des in zip(plabels, pprobs, truelabels, self.pdata.features):
            fullList.append("predicted: {}, actual: {}, predicted prob: {}, description: {}".format(plabel, tlabel, pprob, des))
            if plabel != tlabel:
                wrongList.append("predicted: {}, actual: {}, predicted prob: {}, description: {}".format(plabel, tlabel, pprob, des))
        
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
    p = c3.predict(b2)
    fullList1, wrongList1 = c3.printResult(param="cl2")
    fullList2, wrongList2 = c3.printResult(param="cl1")
