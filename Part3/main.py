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
from spacy.lang.en import English
from scipy.sparse import csr_matrix

queries = [
    "Marvel",
    "X-Men Marvel",
    "X-Men Wolverine epic",
    "Spiderman Avengers crossover",
    "Spiderman Wolverine comic",
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

    intval = int(val)-1
    if intval>=len(queries):
        return ""
    runQuery(queries[intval])
    return val

def runQuery(query):
    count_query, tf_idf = getTfIdf(query)
    print("1c_q: ", count_query.todense())

    val = ""
    while(val!="0"):
        similarity = count_query.dot(tf_idf.transpose())
        array_similarity = similarity.toarray()
        index_order = np.argsort(array_similarity)
        displayResults(query,index_order)
        print("\n\nOptions: \n  1) Give User Feedback\n  2) Rerun Query\n  0) Exit")
        val = input("Selection: ")
        if(val=="1"):
            index_rel,index_irel = getFeedback(index_order)
            a = 0.2 * tf_idf[index_rel,:].sum( axis = 0)
            b = 0.2*tf_idf[index_irel,:].sum(axis = 0)
            query_modified = count_query.todense() + a - b
            similarity_qm = query_modified @ tf_idf.transpose()
            index_order = np.argsort(similarity_qm) # from smallest to largest
            index_order_array = csr_matrix(index_order).toarray()
            displayResults(query,index_order_array,"Modified ")
            val = "0"
        if(val=="2"):
            print("\nRerunning query!\n")

def getFeedback(idx_order):
    global list_docs
    top5 = idx_order[0][:5]
    index_rel = list()
    index_irel = list()
    i=1
    val=""
    while(val!=0):
        for idx in top5:
            print(str(i) + ") " + str(list_docs[idx]))
            feedback = input("Is this accurate?\n  1) Yes\n  2) No\nSelection: ")
            if(feedback is "1"):
                index_rel.append(idx)
            else:
                index_irel.append(idx)
            i=i+1
        
        print("Relevant Indices: " + str(index_rel))
        print("Irrelevant Indices: " + str(index_irel))
        val = input("Is the above output correct?\n  1) Yes\n  2) No\nSelection: ")
        if val=="1":
            break
        print("\n\nRerunning Feedback")
        index_rel.clear()
        index_irel.clear()
        i=1
    print("\nPrecision: " + str(float(len(index_rel)/5)))
    return index_rel,index_irel

def displayResults(query, idx_order, title="Query",flag=False):
    global list_docs
    top5 = idx_order[0,:5]
    i=1
    print(title + "Results for \"" + query + "\" :")
    for idx in top5:
        print(str(i) + ") " + str(list_docs[idx]))
        i=i+1

def getTfIdf(query):
    list_docs_text = [x.review_text for x in list_docs]
    vectorizer = CountVectorizer()
    count_vect = vectorizer.fit_transform(list_docs_text)
    count_query = vectorizer.transform([ query ])
    transformer = TfidfTransformer(norm = None, sublinear_tf = True)
    tf_idf = transformer.fit_transform(count_vect)
    return count_query, tf_idf

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
        result = self.review_text.split()[:20]
        result = self.title[:25] + "... -> " + " ".join(result) + "..."
        return result

    def __getitem__(self):
        return ""

# MAIN
list_docs = list()
def main():
    global list_docs
    
    target = "graphic_novel_final.json"
    list_docs = getDocs(target,10000)
    val = ""
    while val != "exit":
        val = selectQuery()
    print("Program Terminating...")


main()
