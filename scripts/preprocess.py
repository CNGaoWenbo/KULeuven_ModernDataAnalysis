# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 18:14:35 2021

@author: jordan
"""

import os
import re
import pandas as pd
import pycountry

from mydictionary import *

class preprocess:
    def __init__(self):
        #self.data_folder = data_folder
        self.docs=[]
        self.files = {}
        self.countries = {}
        self.years = {}
        self.countries_years = {}
        

        
    def readFile(self,data_folder):
        #data_folder = self.data_folder
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



    def get_who_region(self,country):
        
        for region in who_regions:
            if country in who_regions[region]:
                return region
        if "..." in country:
            abrev_country_name = re.search(r'(?<=^)[^\.]+', country)[0]
            for region in who_regions:
                for c in who_regions[region]:
                    if re.match(abrev_country_name, c):
                        return region
        print("Country not found among WHO regions: %s" % country)
        return False
    
import pathlib
import glob
import csv
from collections import defaultdict
class FileCsvExport:
    """Generate a CSV file containing the name and contents of all files found"""
    def __init__(self, directory: str, output: str, header = None, file_mask = None, walk_sub_dirs = True, remove_file_extension = True):
        self.directory = directory
        self.output = output
        self.header = header
        self.pattern = '**/*' if walk_sub_dirs else '*'
        if isinstance(file_mask, str):
            self.pattern = self.pattern + file_mask
        self.remove_file_extension = remove_file_extension
        self.rows = 0

    def export(self) -> bool:
        """Return True if the CSV was created"""
        return self.__make(self.__generate_dict())

    def __generate_dict(self) -> defaultdict:
        """Finds all files recursively based on the specified parameters and returns a defaultdict"""
        csv_data = defaultdict(list)
        for file_path in glob.glob(os.path.join(self.directory, self.pattern),  recursive = True):
            path = pathlib.Path(file_path)
            if not path.is_file():
                continue
            content = self.__get_content(path)
            name = path.stem if self.remove_file_extension else path.name
            csv_data[name].append(content)
        return csv_data

    @staticmethod
    def __get_content(file_path: str) -> str:
        with open(file_path,encoding='utf8',errors='ignore') as file_object:
            return file_object.read()

    def __make(self, csv_data: defaultdict) -> bool:
        """
        Takes a defaultdict of {k, [v]} where k is the file name and v is a list of file contents.
        Writes out these values to a CSV and returns True when complete.
        """
        with open(self.output, 'w', newline = '',encoding='utf8',errors='ignore') as csv_file:
            writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
            if isinstance(self.header, list):
                writer.writerow(self.header)
            for key, values in csv_data.items():
                for duplicate in values:
                    writer.writerow([key, duplicate])
                    self.rows = self.rows + 1
        return True