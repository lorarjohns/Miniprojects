#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 00:31:47 2019

@author: lorajohns
"""

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import pandas as pd
#import textacy
import spacy
# import time

from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

#url = "https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY"
#page = requests.get(url)
#soup = BeautifulSoup(page.text, "html.parser")

#print(soup.prettify)

class Jobs:
    
    def __init__(self, url):
        
        self.jobtitle = []
        self.company = []
        self.summary = []
        self.salary = []
        self.url = url
        self.next_url = f"&start="
    
    #def __call__(self, **kwargs):
    #   return self.soup
   
    def get_titles(self, iters):
        for page in self.get_next(iters):
            soup = self.soup
            for tag in soup.select("div.title > a.jobtitle"):
                self.jobs.append(tag["title"])
                
    def get_all(self, iters):
        jobtitle = []
        company = []
        summary = []
        salary = []
        
        for soup in self.get_next(iters):
            for job in soup.select("div.jobsearch-SerpJobCard"):
                ti = job.select("div.title > a.jobtitle")
                jobtitle.append(ti["title"])
                co = job.select("span.company")
                company.append(co.text)
                su = job.select("div.summary")
                summary.append(su.text)
                sal = job.select("div.salarySnippet")
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
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        return soup

        
class NLP:
    
    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_md")
        self.ngrams = []
        
    def preprocess(self, text):
        #from textacy import preprocessing
        #text = preprocessing.normalize_whitespace(preprocessing.remove_punct(text))
        doc = self.nlp(text)
        doc = [token for token in doc if not token.is_stop]

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
        y_test = le.fit_transform(y)
        
        return X_train, X_test, y_train, y_test
        
            
__name__ == "__main__"


# text = textacy.text_utils.KWIC(text, "language", window_width=35)

# page.select("div.jobsearch-SerpJobCard > div.title > a[href]")



# <div class="jobsearch-SerpJobCard unifiedRow row result clickcard vjs-highlight" id="pj_9719f8c6eec624f2" data-jk="9719f8c6eec624f2" data-empn="9613973026691547" data-ci="108409095">


n [20]: j = Jobs("https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY")

j.get_all(2)