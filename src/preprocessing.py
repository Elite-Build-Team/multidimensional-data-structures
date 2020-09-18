import string
from os import listdir
from os.path import isfile, join
import re



# returns a list of filepaths and a list of filenames
def returnListOfFilePaths(folderPath):
    fileInfo = []
    listOfFileNames = [fileName for fileName in listdir(folderPath) if isfile(join(folderPath, fileName))]
    listOfFilePaths = [join(folderPath, fileName) for fileName in listdir(folderPath) if
                       isfile(join(folderPath, fileName))]
    fileInfo.append(listOfFileNames)
    fileInfo.append(listOfFilePaths)
    return fileInfo


def removePunctuationFromTokenized(contentsRaw):
    excludePuncuation = set(string.punctuation)

    # manually add additional punctuation to remove
    doubleSingleQuote = '\'\''
    doubleDash = '--'
    doubleTick = '``'

    excludePuncuation.add(doubleSingleQuote)
    excludePuncuation.add(doubleDash)
    excludePuncuation.add(doubleTick)

    filteredContents = [word for word in contentsRaw if word not in excludePuncuation]
    filtered = ""
    for i in filteredContents:
        filtered += i
    doc = filtered.replace("\n", " ").replace("\t", " ")
    new = re.sub('\s+', ' ', doc).strip()
    return new


# converts all letters to lowercase
def convertItemsToLower(contentsRaw):
    filteredContents = [term.lower() for term in contentsRaw]
    return filteredContents


# Creates a content dictionary with all the files to be processed and opens them
def readContent(folderRaw):
    rawContent = []
    for txtfile in folderRaw:
        with open(txtfile, "r", encoding="utf-8", errors='ignore') as ifile:
            fileCont = ifile.read()
        rawContent.append(fileCont)
    return rawContent


# collect all preprocess functions and execute them as one.
def preProcess(rawContentdata):
    lista = []
    for j in rawContentdata:
        unpuncted = removePunctuationFromTokenized(j)
        unpunctedDict = ""
        listaUnpuncted = []
        for k in unpuncted:
            unpunctedDict += k
        listaUnpuncted.append(unpunctedDict)

        for i in listaUnpuncted:
            allLower = convertItemsToLower(i)
            forConvert = ""
            for d in allLower:
                forConvert += d
        new = forConvert.split("/n")
        for i in new:
            lista.append(i)
    return lista


def main():
    print("Please give me the folder path(absolute path) with the files to be preprocessed.")
    inputfile = input()
    baseFolderPath = inputfile

    fileNames, filePathList = returnListOfFilePaths(baseFolderPath)

    rawContentDict = readContent(filePathList)

    processed = preProcess(rawContentDict)

    data = open("data.txt", "w+")
    print("data.txt created.")

    ren = len(fileNames)
    for i in range(ren):
        data.write(fileNames[i] + " " + processed[i] + "\n")


main()
