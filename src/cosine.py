import nltk
import time
import string
import numpy as np
import heapq

# used for looping through folders/files
from os import listdir
from os.path import isfile, join

# Calc tfidf and cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# All text entries to compare will appear here
BASE_INPUT_DIR = "../Documents"


# Returns the folder path/name and its files
def returnListOfFilePaths(folderPath):
    fileInfo = []
    listOfFileNames = [fileName for fileName in listdir(folderPath) if isfile(join(folderPath, fileName))]
    listOfFilePaths = [join(folderPath, fileName) for fileName in listdir(folderPath) if
                       isfile(join(folderPath, fileName))]
    fileInfo.append(listOfFileNames)
    fileInfo.append(listOfFilePaths)
    return fileInfo


# Creates a content dictionary with all the files to be processed and opens them
def create_docContentDict(filePaths):
    rawContentDict = {}
    for filePath in filePaths:
        with open(filePath, "r", encoding="ISO-8859-1") as ifile:
            fileContent = ifile.read()
        rawContentDict[filePath] = fileContent
    return rawContentDict


# Tokenizer function. Returns tokenized data
def tokenizeContent(contentsRaw):
    tokenized = nltk.tokenize.word_tokenize(contentsRaw)
    return tokenized


# Removing unnecessary stopwords
def removeStopWordsFromTokenized(contentsTokenized):
    stop_word_set = set(nltk.corpus.stopwords.words("english"))
    filteredContents = [word for word in contentsTokenized if word not in stop_word_set]
    return filteredContents


# Extra text normalization
def performPorterStemmingOnContents(contentsTokenized):
    porterStemmer = nltk.stem.PorterStemmer()
    filteredContents = [porterStemmer.stem(word) for word in contentsTokenized]
    return filteredContents


# Removing punctuation/extra text normalization
def removePunctuationFromTokenized(contentsTokenized):
    excludePuncuation = set(string.punctuation)

    # manually add additional punctuation to remove
    doubleSingleQuote = '\'\''
    doubleDash = '--'
    doubleTick = '``'
    newLine = '/n'

    excludePuncuation.add(doubleSingleQuote)
    excludePuncuation.add(doubleDash)
    excludePuncuation.add(doubleTick)
    excludePuncuation.add(newLine)

    filteredContents = [word for word in contentsTokenized if word not in excludePuncuation]
    return filteredContents


# Make all terms lower letter format
def convertItemsToLower(contentsRaw):
    filteredContents = [term.lower() for term in contentsRaw]
    return filteredContents


# Process data without writing inspection file information to file
def processData(rawContents):
    cleaned = tokenizeContent(rawContents)
    cleaned = removeStopWordsFromTokenized(cleaned)
    cleaned = performPorterStemmingOnContents(cleaned)
    cleaned = removePunctuationFromTokenized(cleaned)
    cleaned = convertItemsToLower(cleaned)
    return cleaned


# TODO: modify this to build matrix then print from matrix form
def calc_and_print_CosineSimilarity_for_all(tfs, fileNames):
    # print(cosine_similarity(tfs[0], tfs[1]))
    print("\n\n\n========COSINE SIMILARITY====================================================================\n")
    numFiles = len(fileNames)
    names = []
    print('                   ', end="")  # formatting
    for i in range(numFiles):
        if i == 0:
            for k in range(numFiles):
                print(fileNames[k], end='   ')
            print()

        print(fileNames[i], end='   ')
        for n in range(numFiles):
            # print(fileNames[n], end='\t')
            matrixValue = cosine_similarity(tfs[i], tfs[n])
            numValue = matrixValue[0][0]
            # print(numValue, end='\t')
            names.append(fileNames[n])
            print(" {0:.8f}".format(numValue), end='         ')
            # (cosine_similarity(tfs[i], tfs[n]))[0][0]

    print("\n\n=============================================================================================\n")


# Returns the top K most similar documents that were compared
def calc_and_print_topK(tfs, fileNames):
    numFiles = len(fileNames)
    threshold = 0.4
    for i in range(len(fileNames)):
        for n in range(len(fileNames)):
            matrix = cosine_similarity(tfs[i], tfs[n])
            if (matrix[0][0] >= threshold):
                print(fileNames[i] + " " + fileNames[n])


# main calculation starts here    
def main():
    print("Please give me the folder path(absolute path) with the files to be compared.")
    inputfile = input()
    baseFolderPath = inputfile

    fileNames, filePathList = returnListOfFilePaths(baseFolderPath)

    rawContentDict = create_docContentDict(filePathList)

    # calculate tfidf/tfs
    tfidf = TfidfVectorizer(tokenizer=processData, stop_words='english')
    tfs = tfidf.fit_transform(rawContentDict.values())

    t0 = time.time()
    calc_and_print_CosineSimilarity_for_all(tfs, fileNames)
    calc_and_print_topK(tfs, fileNames)
    # print(rawContentDict.values())
    elapsed = (time.time() - t0)
    print("\nTotal Time Elapsed : %.2fsec" % elapsed)


# running the program
main()
