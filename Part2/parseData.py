# Project 1
# Author: William Santos
# Date: 11/4/2019
# Description: This program should only be called once. It will parse the data in the Data 
# folder located in the Project1 folder and write the results to its local Data folder
# The results that Part3 will use are written to Part2's Results folder in a json format.

# IMPORTS
import os
import json
import nltk

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from datetime import datetime

# CLASSES


class Doc:
    def __init__(self, js, nlp):
        self.json = js
        self.rawtext = self.json["review_text"]
        self.text = nlp.processText(self.rawtext)
        self.id = self.json["book_id"]
        self.name = self.json["book_id"]
        self.tfrq = self.termFrequency(self.text)
        self.length = sum(self.tfrq.values())

    def termFrequency(self, t):
        res = dict()
        for i in t:
            if i in res:
                res[i] += 1
            else:
                res[i] = 1
        return res

    def addToGlobalDict(self, d):
        for i in self.tfrq:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        return d

    def addToInvertedIndex(self, d):
        for i in self.tfrq:
            if i in d:
                d[i].append((self.name, self.tfrq[i]))
            else:
                d[i] = list()
                d[i].append((self.name, self.tfrq[i]))
        return d


class NLP_Data:
    def __init__(self, js):
        self.jsFile = js
        # location of the json "id" : "book name"
        path = "../Data/" + "graphic_novels.json"
        print(path)
        f = open(path, 'r')
        self.jsName = json.load(f)
        f.close()
        self.path = "../Data/" + self.jsFile

        # Data Gathering
        self.globalFreq = dict()    # term : globalFreq
        self.invertedIdx = dict()   # term : (name : termFreq)
        self.library = dict()       # name : raw text
        self.topTerms = list()      # list of top terms

        # Statistics
        self.population = 0    # Population
        self.vocabSize = 0     # Vocab Size
        self.maxTermFreq = 0   # highest frequency
        self.minTermFreq = 0   # lowest frequency
        self.topMostFreq = list()   # Top 20 most frequent terms
        self.topLeastFreq = list()  # Top 20 least frequent terms

        # Data Processing
        self.docs = self.startNLP()
        self.getStatistics()
        self.writeNLP_Data()

    def startNLP(self):
        print("test")
        docs = self.gatherData()
        return docs

    def gatherData(self):
        docs = list()
        f = open(self.path, 'r')

        print("Populating Data")
        for line in f:
            self.population = self.population + 1
            rawJson = json.loads(line)
            doc = Doc(rawJson, self)
            if(doc.id in self.jsName):
                doc.name = self.jsName[doc.id]
            print("Appending Doc " + str(self.population) +
                  " :\t" + doc.name + str(self.population))
            docs.append(doc)

        f.close()

        idx = 0
        print("Updating Frequencies")
        for doc in docs:
            self.library[doc.name] = doc.rawtext
            self.globalFreq.update(doc.addToGlobalDict(self.globalFreq))
            self.invertedIdx.update(doc.addToInvertedIndex(self.invertedIdx))
            self.topTerms = sorted(self.globalFreq.items(), key=lambda kv: kv[1], reverse=True)
            idx = idx + 1
            print("Frequency Processing Progress: " + str(round(idx/self.population*100, 2)) + "%")

        return docs

    def getStatistics(self):
        self.vocabSize = len(self.topTerms)
        self.maxTermFreq = self.topTerms[0]
        self.minTermFreq = self.topTerms[-1]
        self.topMostFreq = self.topTerms[:20]
        self.topLeastFreq = list(reversed(self.topTerms[-20:]))

    ### Write_NLP_Data
    def writeNLP_Data(self):
        self.writeToResults()
        self.writeToJson()
        self.writeToMD()

    def writeToResults(self):
        folder = "Results"
        if not os.path.exists(folder):
            os.makedirs(folder)

        files = ["globalFreq.txt", "invertedIdx.txt"]
        titles = ["Global Frequency", "Inverted Index"]
        filepaths = [(folder + "/" + x) for x in files]
        fdict = [self.globalFreq, self.invertedIdx]

        i = 0
        for path in filepaths:
            f = open(path, "w", encoding="utf-8")
            f.write("Assignment 3: " + titles[i] + "\nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\n\n" + titles[i] + ":")
            self.getDictSpacing(f, fdict[i])
            f.close()
            i += 1

        f = open(folder + "/topTerms.txt", "w", encoding="utf-8")
        f.write("Assignment 3: Top Terms\nAuthor: William Santos \nDate " + datetime.today().strftime('%m-%d-%Y') + "\n\nTop Terms in Dataset:")
        for x in self.topTerms:
            f.write("\n" + x[0] + " :\t" + str(x[1]))
        f.close()

    def writeToJson(self):
        folder = "Data"
        if not os.path.exists(folder):
            os.makedirs(folder)
        files = ["globalFreq.json", "invertedIdx.json", "topTerms.json"]
        data = [ self.globalFreq, self.invertedIdx, self.topTerms ]
        filepaths = [(folder + "/" + x) for x in files]
        
        idx=0
        for path in filepaths:
            f = open(path, "w", encoding="utf-8")
            json.dump(data[idx],f)                                            
            f.close()
            idx = idx + 1

    def writeToMD(self):
        fileTarget = "Results.md"
        f = open(fileTarget, 'w')
        f.write("# JSON Stats")
        f.write("\n\n\tTotal JSON Entries: " + str(self.population) + " entries")
        f.write("\n\tVocab Size: " + str(self.vocabSize) + " words")
        f.write("\n\tMax Term Frequency: " + str(self.maxTermFreq))
        f.write("\n\tMin Term Frequency: " + str(self.minTermFreq))

        f.write("\n\n## Top 20 Most Frequent Terms")
        self.writeToMD_List(f,self.topMostFreq)
        f.write("\n\n## Top 20 Least Frequent Terms")
        self.writeToMD_List(f,self.topLeastFreq)
        f.close()

    def writeToMD_List(self, f, l):
        idx = 1
        for x in l:
            line = "\n\t" + str(idx) + ".\t" + x[0] + " : "+ str(x[1])
            f.write(line)
            idx = idx + 1

    def getDictSpacing(self, f, fdict):
        for x in fdict:
            line = "\n" + x + "\t" + self.getSpacing(x) + ": " + str(fdict[x])
            f.write(line)

    def getSpacing(self, x):
        tabs = ""
        space = [4, 8, 12, 16, 20]
        for i in space:
            if(len(x) < i):
                tabs += "\t"
        return tabs
    
    ### Write_NLP_Data END

    ### NLP_Processing
    def fixTag(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    # Output a list of cleaned tokens
    def processText(self, text):
        all_tokens = word_tokenize(text)  # convert to tokens
        all_pos_tags = pos_tag(all_tokens)  # tag tokens

        # Convert to Lower Case
        lower_tokens = [t.lower() for (t, pos) in all_pos_tags]

        # Remove Stopwords
        stoplist = stopwords.words('english')
        stoplist.extend([">", "<", ")", "(", "``", "''",".", "'", ";", "'s", ",", "n't",":","-","!","?","...","'ve","'m","'re","'ll","'d","--"])
        stoplist_tokens = [t for t in lower_tokens if t not in stoplist]
        stoplist_tokens = " ".join(stoplist_tokens)

        # Stem the words
        lemmatizer = WordNetLemmatizer()
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(stoplist_tokens))
        wn_tagged = map(lambda x: (x[0], self.fixTag(x[1])), nltk_tagged)
        result = []
        for word, tag in wn_tagged:
            if tag is None:
                result.append(word)
            else:
                result.append(lemmatizer.lemmatize(word, tag))

        return result
    ### NLP_Processing END

# MAIN
def main():
    NLP_Data("graphic_novel_reviews.json")

main()
