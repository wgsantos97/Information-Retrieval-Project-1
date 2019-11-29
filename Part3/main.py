# imports
import os
import json
# sklearn imports
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# nltk imports
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
import spacy

queries = [
    "Superman art series design",
    "Batman Hush art",
    "DC series good",
    "Superman Batman comic crossover",
    "Superman Batman best crossover comic",
]

# FUNCTIONS
def nlp_processing(doc):
    stoplist = stopwords.words('english')
    lemmatizer = spacy.lang.en.English()
    tokens = lemmatizer(doc)
    terms_no_stop = [
        token.lemma_ for token in tokens if token.lemma_ not in stoplist]
    terms_alnum = [t for t in terms_no_stop if t.isalpha()]
    return terms_alnum


def displayQueryMenu():
    print("Information Retrieval Project 1: Part III - Query Processor")
    print("Please select one of the following by number value\n")
    idx = 1
    for query in queries:
        print(str(idx) + ") - \"" + query + "\"")
        idx = idx + 1
    print("0) - Exit\n")


def selectQuery():
    displayQueryMenu()
    val = input("Selection: ")
    
    if(val=="0"):
        return "exit"
    
    try:
        intval = int(val)-1
        if intval>=len(queries):
            return ""
        runQuery(queries[intval])
        return val
    except ValueError:
        return ""

def getTfIdf(query):
    list_docs_text = [x.review_text for x in list_docs]
    vectorizer = CountVectorizer(tokenizer = nlp_processing)
    count_vect = vectorizer.fit_transform(list_docs_text)
    count_query = vectorizer.transform(query)
    transformer = TfidfTransformer(norm = None, sublinear_tf = True)
    tf_idf = transformer.fit_transform(count_vect)
    return count_query, tf_idf

def runQuery(query):
    print("\n")
    count_query, tf_idf = getTfIdf(query)
    similarity = count_query.dot(tf_idf.transpose())
    array_similarity = similarity.toarray()
    index_order = np.argsort(array_similarity)
    print("Doc Index: ", index_order, index_order.shape)
    print("Query Similarity: ", array_similarity)
    print("Ordered Similarity: ", array_similarity[0,index_order[0,::-1]])
    print("Ordered Doc Index: ", index_order[0,::-1])

def getDocs(filename, cap=50000):
    result = list()
    f = open(filename)
    idx = 0
    for line in f:
        if idx==cap:
            break
        d = json.loads(line)
        r = Review(d)
        result.append(r)
        idx = idx + 1
        print("Progress: [IDX #" + str(idx) + "] - " + str(round(idx/cap*100, 5)) + "%")
    f.close()
    print("\n")
    return result

class Review:
    def __init__(self, js):
        self.book_id = js["book_id"]
        self.title = js["title"]
        self.rating = int(js["rating"])
        self.sentiment = int(js["sentiment"])
        self.review_text = js["review_text"]
    
    def __repr__(self):
        return self.title

# MAIN
list_docs = list()
def main():
    target = "graphic_novel_final.json"
    list_docs = getDocs(target,1000)
    input = ""
    while input != "exit":
        input = selectQuery()
    print("Program Terminating...")


main()
