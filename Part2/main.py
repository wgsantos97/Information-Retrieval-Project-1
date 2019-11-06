# Project 1
# Author: William Santos
# Date: 11/4/2019
# Description:

import os
import json

class Query:
    def __init__(self, q):
        self.query = q
        self.terms = q.lower().split()
        self.tfrq = dict()
        self.tfrq = self.initTRFQ()
    
    def initTRFQ(self):
        res = dict()
        for term in self.terms:
            if term in self.tfrq:
                continue
            else:
                res[term] = 0
        return res

def searchGlobalFreq(queries):
    path = "Data/globalFreq.json"
    f = open(path, 'r')
    globalFreq = json.load(f)
    f.close()

    idx = 0
    keys = len(globalFreq.keys())
    for key in globalFreq:
        for query in queries: # for each query object
            if key in query.tfrq: # check if key exists
                query.tfrq[key] = globalFreq[key]
        idx = idx + 1
        print("Search Progress: " + str(round(idx/keys*100, 2)) + "%")

    return queries

def writeResults(search):
    path = "Results.md"
    f = open(path, 'a')
    f.write("\n\n## Query Results")
    for query in search:
        f.write("\n\n### Query: \"" + query.query + "\"")
        idx = 1
        for (k,v) in query.tfrq.items():
            f.write("\n\t" + str(idx) + ".\t[ " + k + " : " + str(v) + " ]")
            idx = idx + 1
    f.close()

def main():
    queries = [
        "Superman art series design",
        "Batman Hush art",
        "DC series good",
        "Superman Batman comic crossover",
        "Superman Batman best crossover comic",
    ]

    search = list()
    for q in queries:
        search.append(Query(q))
    search = searchGlobalFreq(search)
    writeResults(search)

main()
