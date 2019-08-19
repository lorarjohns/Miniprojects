#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 00:31:47 2019

@author: lorajohns
"""

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
#import textacy
#from textacy import preprocessing

import spacy
# import time

from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

class Jobs:
    
    def __init__(self, job):
        
        self.jobtitle = []
        self.company = []
        self.summary = []
        self.salary = []
        self.url, self.max_iters = self.get_url(job)
        self.next_url = f"&start="
       
    def get_url(self, job):
        job_str = "+".join([word for word in job.split()])
        url = f'https://www.indeed.com/jobs?q="{job_str}"'
        soup = self.get_js(url)
        max_iters = int(soup.select_one("div#searchCount").text.split()[-2].replace(",",""))//10+1
        
        return url, max_iters
        
                
    def get_all(self, max_iters=True):
        
        if max_iters:
            iters = self.max_iters
        else:
            iters = int(input("enter number of pages to fetch: "))
            
        jobtitle = []
        company = []
        summary = []
        salary = []
        
        for soup in self.get_next(iters):
            for job in soup.select("div.jobsearch-SerpJobCard"):
                ti = job.select_one("div.title > a.jobtitle")
                jobtitle.append(ti["title"])
                co = job.select_one("span.company")
                company.append(co.text)
                su = job.select_one("div.summary")
                summary.append(su.text)
                sal = job.select_one("div.salarySnippet")
                try:
                    salary.append(sal.span.text)
                except:
                    salary.append(0)
        
        df = pd.DataFrame({"title":jobtitle, "company":company, 
                      "summary":summary, "salary":salary})
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if type(x) == str else x)
        return df
                

    def get_next(self, iters):
        soups = []
        for i in range(0, iters):
            num = i*10
            url = self.url + self.next_url + str(num)
            #page = requests.get(url)
            #soup = BeautifulSoup(page.text, "html.parser")
            soup = self.get_js(url)
            soups.append(soup)
        return soups
    
    def get_js(self, url):
        '''
        Get webpage with dynamic js container
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        return soup

        
class NLP:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.ngrams = []
       
    def remove_punct(self, text):
        return textacy.preprocessing.normalize_whitespace(textacy.preprocessing.remove_punct(text))
    
    def tokenize(self, text):
        doc = self.nlp(text)
        doc = [token for token in doc if not token.is_stop]

        return doc
    
    def preprocess(self, text):
        text = self.remove_punct(text)
        doc = self.tokenize(text)
        return doc
        
    def ngrams(self, doc, n):
        return list(textacy.extract.ngrams(doc,n))
    
    def encode(self, df):
        '''
        split DF into testing and training
        label encode the target variable
        '''
        X_train, X_test, y_train, y_test = model_selection.train_test_split(df["jobtitle"], df["summary"])
        le = preprocessing.LabelEncoder()
        y_train = le.fit_transform(y_train)
        y_test = le.fit_transform(y_test)
        
        return X_train, X_test, y_train, y_test
        
            
if __name__ == "__main__":
    j = Jobs("Data Scientist")
    df = j.get_all()
    df.to_csv(path_or_buf="indeed.csv", index=False)

# text = textacy.text_utils.KWIC(text, "language", window_width=35)

# page.select("div.jobsearch-SerpJobCard > div.title > a[href]")



# <div class="jobsearch-SerpJobCard unifiedRow row result clickcard vjs-highlight" id="pj_9719f8c6eec624f2" data-jk="9719f8c6eec624f2" data-empn="9613973026691547" data-ci="108409095">


#j = Jobs("https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY")

#j.get_all(2)