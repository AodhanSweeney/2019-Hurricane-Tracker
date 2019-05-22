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






if __name__ == '__main__':
    fileLines = readUrlFile("http://ftp.nhc.noaa.gov/atcf/index/storm_list.txt")
    print(split_storm_info(fileLines))
