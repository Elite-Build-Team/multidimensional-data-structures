from __future__ import division
import sys
import random
import time
import binascii

# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.
numHashes = 10

dataFile = 'data.txt'

numDocs = sum(1 for line in open('data.txt'))

docNames = []

docsAsShingleSets = {}
signatures = []

numElems = int(numDocs * (numDocs - 1) / 2)

JSim = [0 for x in range(numElems)]
estJSim = [0 for x in range(numElems)]


def shingleDocs():
    print("Shingling articles...")

    f = open(dataFile, "rU")

    t0 = time.time()

    totalShingles = 0

    for i in range(0, numDocs):
        # Read all of the words (they are all on one line) and split them by white
        # space.
        words = f.readline().split(" ")
        docID = words[0]
        docNames.append(docID)
        del words[0]

        shinglesInDoc = set()
        # Construct the shingle text by combining three words together.
        for index in range(0, len(words) - 2):
            shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
            # Hash the shingle to a 32-bit integer.
            crc = binascii.crc32(str.encode(shingle)) & 0xffffffff
            # Add the hash value to the list of shingles for the current document. 
            # Note that set objects will only add the value to the set if the set
            # doesn't already contain it.
            shinglesInDoc.add(crc)
        # Store the completed list of shingles for this document in the dictionary.   
        docsAsShingleSets[docID] = shinglesInDoc

        # Count the number of shingles across all documents.
        totalShingles = totalShingles + (len(words) - 2)

    f.close()

    print('\nShingling ' + str(numDocs) + ' docs took %.2f sec.' % (time.time() - t0))

    print('\nAverage shingles per doc: %.2f' % (totalShingles / numDocs))


# Define virtual Triangle matrices to hold the similarity values. For storing
# similarities between pairs, we only need roughly half the elements of a full
# matrix. Using a triangle matrix requires less than half the memory of a full
# matrix, and can protect the programmer from inadvertently accessing one of
# the empty/invalid cells of a full matrix.

def getTriangleIndex(i, j):
    if i == j:
        sys.stderr.write("Can't access triangle matrix with i == j")
        sys.exit(1)
    if j < i:
        temp = i
        i = j
        j = temp

    k = int(i * (numDocs - (i + 1) / 2.0) + j - i) - 1

    return k


# Generate a list of 'k' random coefficients for the random hash functions,
# while ensuring that the same value does not appear multiple times in the 
# list.
def pickRandomCoeffs(k):
    randList = []
    maxShingleID = 2 ** 32 - 1

    # Get a random shingle ID.

    while k > 0:
        randIndex = random.randint(0, maxShingleID)

        # Ensure that each random number is unique.

        while randIndex in randList:
            randIndex = random.randint(0, maxShingleID)

            # Add the random number to the list.

        randList.append(randIndex)
        k = k - 1

    return randList


def minHashSigns():
    # Time this step.
    t0 = time.time()

    print('\nGenerating random hash functions...')

    nextPrime = 4294967311

    # For each of the 'numHashes' hash functions, generate a different coefficient 'a' and 'b'.

    coeffA = pickRandomCoeffs(numHashes)
    coeffB = pickRandomCoeffs(numHashes)

    print('\nGenerating MinHash signatures for all documents...')

    # signatures = []

    # Rather than generating a random permutation of all possible shingles,
    # we'll just hash the IDs of the shingles that are *actually in the document*,
    # then take the lowest resulting hash code value. This corresponds to the index
    # of the first shingle that you would have encountered in the random order.

    for docID in docNames:
        # Get the shingle set for this document.
        shingleIDSet = docsAsShingleSets[docID]

        signature = []

        for i in range(0, numHashes):

            # For each of the shingles actually in the document, calculate its hash code
            # using hash function 'i'.

            # Track the lowest hash ID seen. Initialize 'minHashCode' to be greater than
            # the maximum possible value output by the hash.
            minHashCode = nextPrime + 1

            for shingleID in shingleIDSet:
                # Evaluate the hash function.
                # Our random hash function will take the form of:
                #   h(x) = (a*x + b) % c
                # Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is
                # a prime number just greater than maxShingleID.
                hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
                # Track the lowest hash code seen.
                if hashCode < minHashCode:
                    minHashCode = hashCode
            # Add the smallest hash code value as component number 'i' of the signature.
            signature.append(minHashCode)
        # Store the MinHash signature for this document.
        signatures.append(signature)

    elapsed = (time.time() - t0)

    print("\nGenerating MinHash signatures took %.2fsec" % elapsed)


def signsCompare():
    print('\nComparing all signatures...')

    t0 = time.time()

    for i in range(0, numDocs):
        # Get the MinHash signature for document i.
        signature1 = signatures[i]

        for j in range(i + 1, numDocs):
            # Get the MinHash signature for document j.
            signature2 = signatures[j]

            count = 0
            # Count the number of positions in the minhash signature which are equal.
            for k in range(0, numHashes):
                count = count + (signature1[k] == signature2[k])
            # Record the percentage of positions which matched.
            estJSim[getTriangleIndex(i, j)] = (count / numHashes)

    elapsed = (time.time() - t0)

    print("\nComparing MinHash signatures took %.2fsec" % elapsed)


def displayPairs():
    threshold = 0.5
    print("\nList of Document Pairs with J(d1,d2) more than", threshold)
    print("Values shown are the estimated Jaccard similarity and the actual")
    print("Jaccard similarity.\n")
    print("                        Est. J   Act. J")

    for i in range(0, numDocs):
        for j in range(i + 1, numDocs):
            estJ = estJSim[getTriangleIndex(i, j)]

            if estJ > threshold:
                s1 = docsAsShingleSets[docNames[i]]
                s2 = docsAsShingleSets[docNames[j]]
                J = (len(s1.intersection(s2)) / len(s1.union(s2)))

                print("  %5s --> %5s   %.2f     %.2f" % (docNames[i], docNames[j], estJ, J))


if __name__ == "__main__":
    t0 = time.time()
    shingleDocs()
    minHashSigns()
    signsCompare()
    displayPairs()

    elapsed = (time.time() - t0)
    print("\nTotal Time Elapsed : %.2fsec" % elapsed)
