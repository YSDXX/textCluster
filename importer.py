#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 09:09:18 2018

@author: everitt257
"""

import pickle
import pandas as pd
import os

class importer:
    
    def __init__(self,fileName):
        self.file = fileName
        self.features = None
        self.labels1 = None
        self.labels2 = None
            
    def readfile(self):
        cwd = os.getcwd()
        filePath = os.path.join(cwd,self.file)
        self.myfile = pd.read_excel(filePath)
    
    def parsefile(self,fname="需求描述",l1name="系统名称",l2name="需求类型"):
        self.features = self.myfile["需求描述"]
        self.labels1 = self.myfile["系统名称"]
        self.labels2 = self.myfile["需求类型"]
    
    def savefile(self, name="savedmodel"):
        fileSaved = {"features":self.features,
                     "labels1":self.labels1,
                     "labels2":self.labels2}
        savename = name+'.p'
        pickle.dump(fileSaved, open(savename, "wb"))
    
    def process(self):
        if not os.path.isfile("savedmodel.p"):
            self.readfile()
            self.parsefile()
            self.savefile()
        else:
            print("saved model found")
    
    @staticmethod
    def readsavedFile(name="savedmodel", flag=0):
        savedname = name+'.p'
        try:
            raw_data = pickle.load(open(savedname, "rb"))
            return raw_data
        except:
            raw_data = None
            if flag == 0:
                print("You might forgot to process it/naming it wrong!")
        
    
    def __repr__(self):
        return "file name is: %s" % self.file
    
    
if __name__ =='__main__':

    fileName = "1月1日-12月17日上报网公司周报工单详情.xlsx"
    test = importer(fileName)
    test.process()
    raw = test.readsavedFile()
    
    
    