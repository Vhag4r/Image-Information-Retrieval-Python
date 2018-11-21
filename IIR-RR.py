# -*- coding: utf-8 -*-
"""
@author: Ross Fung
@title                  Information Retrieval - Ranked Retrieval 
"""

import re 
import os
import math
import operator

DELIM = '[ \r\n\t0123456789;:.,/\(\)\"\'-]+' #Delimiter used in tokenization to determine how to split strings

def tokenize(text):
    return re.split(DELIM, text.lower()) 

def readfile(path, docid):
    files = sorted(os.listdir(path))
    f = open(os.path.join(path, files[docid]), 'r')
    s = f.read()
    f.close()
    return s

# A function taking the path location of input documents,
# matching a word with term frequency within the document.
    
def indextextfiles_RR(path):
    N = len(sorted(os.listdir(path))) #Get document count from path
    wordCounts = {} #Initialize empty dictionary 
    for docID in range(N): #For each document
        wordCounts[docID] = {}  #Create new dictionary for storing word frequency for each document
        s = readfile(path, docID) #Scan in document contents
        words = tokenize(s) #Split and tokenize each word
        for w in words: 
            if w!='':  #Whitespace check
                if w not in wordCounts[docID]: #If word not present in document dictionary create new key-value pair
                    wordCounts[docID][w] = 1 #Set new count to 1 
                else:
                    wordCounts[docID][w] += 1 #Increment current count by 1 if key-value pair exists for a word
    return wordCounts


#  A ranked retrival query returning k number of results best matching
#  an input query, based on the the tf-idf weighting scheme.
    
def query_RR(wordCounts,query,k):
    N = len(wordCounts.keys()) #Get total number of documents within the collection
    queryWords = tokenize(query) #Tokenize query allowing for splitting and searching word by word
    docScore = [] #Create an empty array for storing docID-value pairs
    for docID in range(N): #For each document 
        docTotal = 0 
        for word in queryWords: #For each word in the query
            df = 0 #Initialize document frequency & term frequency to 0
            tf = 0
            if word in wordCounts[docID]: #Check if the word exists in the given document
                  tf = wordCounts[docID][word] #Get term frequency within document 
            for ID in range(N): #Get document frequency of a word 
                if word in wordCounts[ID]: #Check if word exists in each document
                    df += 1 #If word exists within the document increment count by 1
            if(df!=0):
                idf = math.log(N/df,10) #Calculate inverse document freqency from document frequency df
            else:
                idf = 0
            wordScore = tf*idf #Calculate product of term-frequency and inverse-document frequency for this word
            docTotal += wordScore #Add to document Total
        docScore.append([docID,docTotal])   #After all words valued and summed store score with document ID
        
    sorted_score = sorted(docScore,key=operator.itemgetter(1)) #Sort score array based on the score of the document
    sorted_docs = [] 
    start = N - k #Start the array slice at the top N-K results
    for i in sorted_score[start:]: #For each result in top k slice 
        sorted_docs.append(i[0]) #Add DocumentID to returned array
    print query 
    print sorted_docs,'\n'
    return sorted_docs
    
counts = indextextfiles_RR('docs')
query_RR(counts,'metric used', 10)
query_RR(counts,'more than one', 20)
query_RR(counts,'england played very well', 20)
query_RR(counts,'the next phase', 5)
