# -*- coding: utf-8 -*-
"""
Created on Sat May  8 03:00:14 2021

@author: jordan
"""
# Search for climate key words on each document
from mydictionary import *
from nltk.tokenize import MWETokenizer
import re
import preprocess
class climateKeywords:
    def __init__(self):
        self.per_country = {}
        self.per_country_focusyear = {}
        self.average_per_country_focusyear = {}
        self.proportion_per_country_focusyear = {}
        self.per_year = {}
        self.average_per_year = {}
        self.proportion_per_year = {}
        self.per_region = {}
        self.per_region_year = {}
        self.proportion_per_region_year = {}
        self.histogram_number_of_mentions = {}
        
        
        self.global_count_climate_keywords = {}
        self.per_year_count_climate_keywords = {}
        self.global_climate_contexts = []
        
        self.cooccurrence_matrix = {}
        
        

    def get_context(self,index, wordlist):
        lowest_index = max(0, index-25)
        highest_index = min(index+1+25, len(wordlist))
        return wordlist[lowest_index:index] + wordlist[index+1:highest_index]
    

    
    def getResults(self,docs,files,countries,years,countries_years,focus_year,regions_years):
        tokenizer = MWETokenizer(compound_terms)
        # A ``MWETokenizer`` takes a string which has already been divided into tokens and
        # retokenizes it, merging multi-word expressions into single tokens
        regex = re.compile(r'^.{1,3}$') #words with 3 or less chars
        for termset in ["climate"]:
            self.per_country[termset] = {}
            self.per_country_focusyear[termset] = {}
            self.average_per_country_focusyear[termset] = {}
            self.proportion_per_country_focusyear[termset] = {}
            self.per_year[termset] = {}
            self.average_per_year[termset] = {}
            self.proportion_per_year[termset] = {}
            self.per_region[termset] = {}
            self.histogram_number_of_mentions[termset] = {}
            
        for region in who_regions.keys():
            self.per_region_year[region] = {}
            self.proportion_per_region_year[region] = {}
        
        for file in files.keys():
            print("Loading %s" % (file))
        
            try:
                txtFileObj = open(file, encoding='utf8')
            except:
                print('Could not open file %s' % file)
        
            wordlist = re.split(r'[\W0-9]+', txtFileObj.read().lower())
            compounds_wordlist = tokenizer.tokenize(wordlist)
            filtered_compounds_wordlist = [w for w in compounds_wordlist if (len(w) > 3)]
        
            climate_contexts = []
            year = files[file]["year"]
            country = files[file]["country"]
            region = preprocess.preprocess().get_who_region(country)
            
            for i in range(0,len(filtered_compounds_wordlist)):
                word = filtered_compounds_wordlist[i]          
                if word in climate_dict:
                    context = self.get_context(i, filtered_compounds_wordlist)
                    climate_contexts.append(context)
                    self.global_count_climate_keywords[word] = self.global_count_climate_keywords.get(word, 0) + 1
                    #per_year_count_climate_keywords[word][year]= per_year_count_climate_keywords[word].get(year, 0) + 1
                    self.global_climate_contexts.extend(context)       
             
            total_climate_mentions = len(climate_contexts)      
            total_intersection_mentions = 0
                
            self.histogram_number_of_mentions["climate"][total_climate_mentions] = self.histogram_number_of_mentions["climate"].get(total_climate_mentions, 0) + 1  
            self.per_country["climate"][country] = self.per_country["climate"].get(country,0) + total_climate_mentions
            
            if year == focus_year: 
                self.per_country_focusyear["climate"][country] = self.per_country_focusyear["climate"].get(country,0) + total_climate_mentions
               
            if region != False:  
                self.per_region["climate"][region] = self.per_region["climate"].get(region,0) + total_climate_mentions
                self.per_region_year[region][year] = self.per_region_year[region].get(year,0) + total_climate_mentions
            
            self.per_year["climate"][year] = self.per_year["climate"].get(year,0) + total_climate_mentions
            
            if total_climate_mentions > 0:
                self.proportion_per_year["climate"][year] = self.proportion_per_year["climate"].get(year,0) + 1
                if year == focus_year:
                    self.proportion_per_country_focusyear["climate"][country] = self.proportion_per_country_focusyear["climate"].get(country,0) + 1
                if region != False:
                    self.proportion_per_region_year[region][year] = self.proportion_per_region_year[region].get(year,0) + 1
        
        for year in years.keys():
            self.average_per_year["climate"][year] = self.per_year["climate"][year]/years[year]
            self.proportion_per_year["climate"][year] = self.proportion_per_year["climate"].get(year,0)/years[year] * 100
        
        for country in countries_years.keys():
            if focus_year in countries_years[country].keys():      
                self.average_per_country_focusyear["climate"][country] = self.per_country_focusyear["climate"].get(country, 0)/self.countries_years[country][focus_year]
                self.proportion_per_country_focusyear["climate"][country] = self.proportion_per_country_focusyear["climate"].get(country,0)/self.countries_years[country][focus_year] * 100
        
        for region in regions_years.keys():
            for year in regions_years[region].keys():      
                self.proportion_per_region_year[region][year] = self.proportion_per_region_year[region].get(year,0)/regions_years[region][year] * 100        