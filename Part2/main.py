# HW 3
# Author: William Santos
# Date: 9/29/2019
# Description:
#

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
    def __init__(self, js, folder):
        self.jsFile = js
        # location of the json "id" : "book name"
        path = "../" + folder + "/" + "graphic_novels.json"
        print(path)
        f = open(path, 'r')
        self.jsName = json.load(f)
        f.close()
        self.path = "../" + folder + "/" + self.jsFile

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
        self.topMostFreq = 0   # Top 20 most frequent terms
        self.topLeastFreq = 0  # Top 20 least frequent terms

        # Data Processing
        self.docs = self.startNLP()
        self.writeResults()

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
            self.topTerms = sorted(
                self.invertedIdx.items(), key=lambda kv: kv[1])
            print("Frequency Processing Progress: " +
                  str((idx+1)/self.population) + "%")

        return docs

    def writeResults(self):
        folder = "Results"
        if not os.path.exists(folder):
            os.makedirs(folder)

        files = ["globalFreq.txt", "invertedIdx.txt"]
        titles = ["Global Frequency", "Inverted Index"]
        filepaths = [(folder + "/" + x) for x in files]
        fdict = [self.globalFreq, self.invertedIdx]

        i = 0
        for path in filepaths:
            f = open(path, "w")
            f.write("Assignment 3: " + titles[i] + "\nAuthor: William Santos \nDate " + datetime.today(
            ).strftime('%m-%d-%Y') + "\n\n" + titles[i] + ":")
            self.getDictSpacing(f, fdict[i])
            f.close()
            i += 1

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
        stoplist.extend([">", "<", ")", "(", "``", "''",
                         ".", "'", ";", "'s", ",", "n't"])
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


# MAIN
def main():
    nlp = NLP_Data("graphic_novel_reviews.json", "Data")


main()
