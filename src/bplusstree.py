import time
from os.path import isfile, join, dirname
from os import listdir
import string
MYDIR = dirname(__file__) #gives back your directory path

from preprocessing import *

class Node(object):
    '''
    Base node object.
    Each node stores keys and values. Keys are not unique to each value, and
    as such values are stored as a list under each key.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    '''
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.values = []
        self.leaf = True

    def add(self, key, value):
        '''
        Adds a key-value pair to the node.
        '''
        if not self.keys:
            self.keys.append(key)
            self.values.append([value])
            return None

        for i, item in enumerate(self.keys):
            if key == item:
                self.values[i].append(value)
                break

            elif key < item:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self):
        '''
        Splits the node into two and stores them as child nodes.
        '''
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order / 2)

        left.keys = self.keys[:mid]
        left.values = self.values[:mid]

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]

        self.keys = [right.keys[0]]
        self.values = [left, right]
        self.leaf = False

    def is_full(self):
        '''
        Returns True if the node is full.
        '''
        return len(self.keys) == self.order

class BPlusTree(object):
    '''
    B+ tree object, consisting of nodes.
    Nodes will automatically be split into two once it is full. When a split
    occurs, a key will 'float' upwards and be inserted into the parent node to
    act as a pivot.
    Attributes:
        order (int): The maximum number of keys each node can hold.
    '''
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        '''
        For a given node and key, returns the index where the key should be
        inserted and the list of values at that index.
        '''
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i

        return node.values[i + 1], i + 1

    def _merge(self, parent, child, index):
        '''
        For a parent and child node, extract a pivot from the child to be
        inserted into the keys of the parent. Insert the values from the child
        into the values of the parent.
        '''
        parent.values.pop(index)
        pivot = child.keys[0]

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        '''
        Inserts a key-value pair after traversing to a leaf node. If the leaf
        node is full, split the leaf node into two.
        '''
        parent = None
        child = self.root

        while not child.leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        if child.is_full():
            child.split()

            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key,file):
        '''
        Returns a value for a given key, and None if the key does not exist.
        '''
        child = self.root

        while not child.leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child.keys):
            if key == item:
                return child.values[i],file
        print("Not found in:" ,file)
        

def bplustree(dictionary,search,doc):
    bplustree = BPlusTree(order=4)

    for d in dictionary:
        bplustree.insert(d,d)
   
    print (bplustree.retrieve(search,doc))

#find all documents in the theme that was asked
def docs_to_search(path_of_docs):
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
def dict_of_words(doc):
    #words = {}
    file = open(doc, "r", encoding="UTF-8", errors='ignore')
    words = file.read()
    return words 


def main():
    elapsed_time=0.0
    documents = ""
    input_theme = input("Type the theme of documents that you want to search. e.g.atheism,med,space...")
    #example directory C:\Users\lefteris\.spyder-py3 
    path_of_docs = MYDIR +'/data_set/' + input_theme #execute path+files or dataset +file of documents
    #example result of the above live C:\Users\lefteris\.spyder-py3\data_set\alt.atheism
    
    documents = docs_to_search(path_of_docs)
    search = input("Type the word or phrase you are looking for: ")
    #search in every document
    point = 0 #to keep track of which text I am searching into
    for doc in documents[1]:
        raw_dictionary = dict_of_words(doc)
        raw_dictionary = removePunctuation(raw_dictionary)
        dictionary =""
        for r in raw_dictionary:
            dictionary += r
        dictionary = convertItemsToLower(dictionary)
        
        start_time = time.time()
        bplustree(dictionary,search,documents[0][point])
        end_time = time.time()
        elapsed_time += end_time - start_time
        point+=1
    print("epalsed time:",elapsed_time)
    
if __name__ == '__main__':
    main()