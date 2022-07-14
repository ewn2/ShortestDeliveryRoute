import csv
import re


# Caches the relationship between each location from an input csv file to a List, time complexity of O(n) as they are
# imported as rows rather than as individual values
def cacheLocations(csvFileName):
    locationCache = []
    with open(csvFileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            locationCache.append(row[2:])
    return locationCache


# Caches the index of Locations for distance reference from an input csv file to a Dictionary, time complexity of O(n)
def cacheDistances(csvFileName):
    with open(csvFileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        foundStructure = {}
        i = 0
        for row in csvreader:
            regexEdit = re.sub(r'\([^)]*\)||\n||^ ', '', row[1])  # To remove the hub codes
            foundStructure[regexEdit] = i
            i = i + 1
        return foundStructure
