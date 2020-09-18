import time
from os.path import isfile, join, dirname
from os import listdir
import math
from bitarray import bitarray
import string
import murmurhash

from preprocessing import *

MYDIR = dirname(__file__)  #gives back your directory path
"""By building a bit array based upon a dictionary this probabilistic structure
allows searches for probable membership, and certain non-membership of
any lookups within the bloom filter.

Based on the dictionary_file, builds a bit array to 
be used for testing membership within the file for a given
percentage, and accurate non-membership."""


#bloom start
def fillArray(dictionary):
    num_words = len(dictionary)
    array_length, num_hashes = calcOptimalHash(num_words) #count number of hashes
    bit_array = array_length * bitarray('0') #arxikopoihsh bit_array
    for word in dictionary: #gia kathe leksi
        for h in range(num_hashes):  #oses einai oi hash
            hash_index = murmurhash.hash(word, num_hashes) % array_length #hasharw
            bit_array[hash_index] = True #thetw 1 to apotelesma ths hash
            
    return bit_array,array_length,num_hashes


def calcOptimalHash(number_words):
        """Calculate array_length and number of hash functions."""
                
        m = -number_words * math.log(0.01) / math.log(2) ** 2
        array_length = int(m)  #bit_array_length
       
        k = (m / number_words) * 0.3 # 0.3 = ln(2) 
        hashes = int(math.ceil(k)) #num_hashes
        return array_length, hashes

#test if hash gives answer in bitarray
def probableMember(word, num_hashes, array_length,bit_array):
    """Test whether word probably is in the dictionary, or
    are surely not in the dictionary."""
    
    for h in range(num_hashes):
        candidateHash = murmurhash.hash(word, num_hashes) % array_length
        if not bit_array[candidateHash]:
            return False
    return True
#give probabilistic answer
def lookUp(search,num_hashes,array_length, bit_array):
    """Test whether word probably is in the dictionary, or
    are surely not in the dictionary."""
    
    if probableMember(search,num_hashes,array_length, bit_array):
        return'"{}" is most likely in text '.format(search)
    else:
        return '"{}" is surely not in text '.format(search)
    
#bloom end

#find all documents in the theme that was asked
def docsToSearch(path_of_docs):
    file_info = []
    try:
        list_files = [file for file in listdir(path_of_docs) if isfile(join(path_of_docs, file))]
        list_paths = [join(path_of_docs, file) for file in listdir(path_of_docs) if isfile(join(path_of_docs, file))]
        file_info.append(list_files)
        file_info.append(list_paths)
    except FileNotFoundError:
        print("Not a folder, stop the programm and rerun with valid folder name!")
        return file_info
    return file_info

#create dictionary with the words of each document
def dictOfWords(doc):
    words = {}
    file = open(doc, "r", encoding="UTF-8", errors='ignore')
    words = file.read()
    return words 
             
def main():
    documents = ""
    elapsed_time=0.0
    input_theme = input("Type the theme of documents that you want to search. e.g.atheism,med,space...")
    #example directory C:\Users\lefteris\.spyder-py3 
    path_of_docs = MYDIR + "/data_set/" + input_theme #execute path+files or dataset +file of documents
    #example result of the above live C:\Users\lefteris\.spyder-py3\data_set\alt.atheism
    
    documents = docsToSearch(path_of_docs)
    search = input("Type the word you are looking for: ")
    #search in every document
    point = 0 #to keep track of which text I am searching into
    for doc in documents[1]:
        raw_dictionary = dictOfWords(doc)
        raw_dictionary = removePunctuation(raw_dictionary)
        dictionary =""
        for r in raw_dictionary:
            dictionary += r
        dictionary = convertItemsToLower(dictionary)
        #dictionary is now clear for bloom filter application
        start_time = time.time()
        bit_array,array_length,num_hashes = fillArray(dictionary)
        answer = lookUp(search,num_hashes,array_length,bit_array) + documents[0][point]
        end_time = time.time()
        elapsed_time += end_time - start_time
        print(answer)
        point+=1
    print("epalsed time:",elapsed_time)
    
if __name__ == '__main__':
    main()