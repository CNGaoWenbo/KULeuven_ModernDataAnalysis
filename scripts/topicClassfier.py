# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 18:14:35 2021

@author: jordan
"""

import os
import re
import pandas as pd
import pycountry
class preprocess:
    def __init__(self):
        #self.data_folder = data_folder
        self.docs=[]
        self.files = {}
        self.countries = {}
        self.years = {}
        self.countries_years = {}
        

        
    def readFile(self,data_folder):
        
        filename_pattern = re.compile(r"^(?P<country>[A-Z]{2,4})_[0-9]{2}_(?P<year>[0-9]{4}).txt$", re.VERBOSE)
        
        docs=self.docs
        files = self.files
        countries = self.countries
        years = self.years
        countries_years = self.countries_years 
        
        for root, directories, filenames in os.walk(data_folder):
            for filename in filenames: 
                match = filename_pattern.match(filename)
                if match:
                    path = os.path.join(root,filename)
                    with open (path,encoding='utf8',errors='ignore') as fin:
                        if re.match(filename_pattern, filename):
                            doc=fin.read().strip('\n\t')
                            docs.append(doc) 
                        
                    (country, year) = (match.group('country'), match.group('year'))
                    try:
                        country_name = pycountry.countries.get(alpha_3=country).name
                    except:
                        country_name = country
                    files[path] = {'country' : country_name, 'year' : year}
                    countries[country_name] = countries.get(country_name,0) + 1
                    years[year] = years.get(year,0) + 1
                    if country_name in countries_years.keys():
                        countries_years[country_name][year] = countries_years[country_name].get(year,0) + 1
                    else:
                        countries_years[country_name] = {year : 1}
        #print("There are %d speeches in total" % (len(files.keys())))
        
        self.docs = docs
        self.files = files
        self.countries = countries
        self.years = years
        self.countries_years = countries_years
    def getDocs(self):
        return self.docs
    def getFiles(self):
        return self.files
    def getCountries(self):
        return self.countries
    def getCountries_years(self):
       return self.countries_years
   
