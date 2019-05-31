#! /usr/bin/env python
"""This program is written to be a recreation of the 2014 hur_tracker.py
but with updated interface and functionality. Primary goal is to recreate
the hurricane tracking maps

Aodhan Sweeney
Unidata Summer Internship
May 2019
hurricane_tracker_2019.py
"""

import numpy as np
from pandas import DataFrame
import requests
from io import StringIO
import sys


def readUrlFile(url):
    """readUrlFile is a function created to read a data file from a given url
    and compile it into a list of strings."""
    response = requests.get(url)

    data_set = response.text
    string_buffer = StringIO(data_set)
    set = string_buffer.getvalue()
    return(set.splitlines())

def split_storm_info(storm_list):
    """storm_holder takes a list of strings and creates a pandas dataframe
    for the data set taken off the NHC archive."""

    name, cycloneNum, year, stormType, basin, filename = [],[],[],[],[],[]
    for line in storm_list[1:]:
        fields = line.split(",")
        name.append(fields[0].strip())
        basin.append(fields[1].strip())
        cycloneNum.append(fields[7].strip())
        year.append(fields[8].strip())
        stormType.append(fields[9].strip())
        filename.append(fields[-1].strip().lower())

    storms = DataFrame({"Name":name, "Basin":basin, "CycloneNum":np.array(cycloneNum),
                        "Year":np.array(year), "StormType":stormType, "Filename":filename})
    return(storms)

def split_model_info(fileLines):
    """split_model_info is a function that will split the data for the models
    into a pandas dataframe."""
    # Pulling necessary data from lines in file
    model, info = [],[]
    for line in fileLines[1:]:
        model.append(line[4:8].strip())
        info.append(line[68:].strip())

    #Combining data from file into a Pandas Dataframe dictionary.
    models = DataFrame({"Model":model, "Info":info})
    return(models)


def get_storms(year, storms):
    """get_storms is a function that is written to take a user defined year from
    1851 to 2019 and then strim the split_storms_info dataframe to just have
    storms from that year"""
    one_year_table = storms[storms.Year == year]
    return(one_year_table)

def get_models(year, filename):
    """get_models is a function that takes in a storm name from a previously
    selected year"""
    url = "http://ftp.nhc.noaa.gov/atcf/archive/%4s/a%8s.dat.gz" % (year,filename)
    fileLines = readUrlFile(url)
    models = split_model_info(fileLines)
    print(models)






if __name__ == '__main__':
    fileLines = readUrlFile("http://ftp.nhc.noaa.gov/atcf/index/storm_list.txt")
    storms = split_storm_info(fileLines)
    #year = str(input("Enter the year for which to find the storms: "))
    year = str(2017)
    one_year_table = get_storms(year, storms)
    print(one_year_table)
    #Taking the filename from SELMA
    filename = 'ep202017'
    one_storm_model = get_models(year, filename)
