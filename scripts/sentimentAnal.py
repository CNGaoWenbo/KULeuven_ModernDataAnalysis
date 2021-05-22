# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:36:27 2021

@author: wenbo
"""

from afinn import Afinn
import time
import numpy as np
class sentimentAnal:
    def __init__(self,years,files,docs):
        self.years = years
        self.files = files
        self.docs = docs

    def sentence_split(self,str_centence):
        list_ret = []
        for s_str in str_centence.split('.'):
            if '?' in s_str:
                list_ret.extend(s_str.split('?'))
            elif '!' in s_str:
                list_ret.extend(s_str.split('!'))
            else:
                list_ret.append(s_str)
        return list_ret
    
    def getTotalIndex(self,index):
        years = self.years
        indexPerYear = np.zeros(len(years.keys()))
        count = 0
        cur = 0
        for i in years.keys():
            for j in range(years[i]):
                indexPerYear[count] += index[cur]
                cur += 1
            indexPerYear[count] /= j
            count += 1
        return indexPerYear
    
    def getIndexs(self):
        files = self.files
        docs = self.docs
        afinn = Afinn(language='en')
        pos_index = []
        neg_index = []
        neutral_index = []
        
        n_speech = len(files.keys())
        for i in range(n_speech):
            lines = self.sentence_split(docs[i])
            pos = 0
            neg = 0
            neutral = 0
            print("progress:{0}%".format(round((i + 1) * 100 /n_speech)), end="\r")
            time.sleep(0.01)
            for line in lines:
                score = int(afinn.score(line))
                
                if score > 0:
                    pos += 1
                elif score < 0:
                    neg += 1
                else:
                    neutral += 1
                
            n = len(lines)
            pos_index.append(pos / n)
            neg_index.append(neg / n)
            neutral_index.append(neutral / n)
        return pos_index,neg_index,neutral_index
    def vis(self,pos_index,neg_index,neutral_index):
        import matplotlib.pyplot as plt
        import numpy as np
        import matplotlib.ticker as ticker
        
        totPos = self.getTotalIndex(pos_index)
        totNeg = self.getTotalIndex(neg_index )
        totNeu = self.getTotalIndex(neutral_index)
        X = np.arange(1970,2019)
        plt.plot(X,totPos,'-.',label='positve')
        plt.plot(X,totNeg, '--',label='negative')
        plt.plot(X,totNeu,'-',label='neutral')
        plt.legend()
        plt.xticks(X)
        plt.xlabel('year')
        plt.ylabel('Index')
        plt.grid()
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.savefig('../output/sentimentYearTrend.png')
        plt.show()