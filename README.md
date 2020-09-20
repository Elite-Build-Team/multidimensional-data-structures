# multidimensional-data-structures

This project compares:
* The efficiency and the time complexity of Bloom Filter, B+ Tree term search on a document.
* The accuracy and time complexity of document similarity measuring using either LSH or Cosine Similarity methods. 
* A preprocessing module is used as a tool of cleaning the initial text files that are used. Preprocessing formats the documents into a clean format, thus optimizing the algorithms' efficiency.

## Bloom Filter vs B+ Tree
* **Bloom filter** is a probabilistic data structure. This specific filter was implemented for term searching in documents. Every word in each document gets hashed and then inserted into a bit array.
The word we want to search gets hashed
and the results are compared to the bit array of each word in the document. If all
positions showing this result are "1" in the bit array then
the filter's answer is that most likely this word will
exist in the corresponding text. If even one bit is "0", then
we conclude that this word certainly does not exist in
this text.
* **B+ Tree** is a data structure that places data
at nodes interconnected by parent - child relations.
A search is made by comparing their pointers to lower nodes until
the leafs on which the information is
stored are reached. There are pointers between the leaves,
thus creating a chain, for faster search
so that no back - steps are taken. 
* **The comparison** between the 2 search methods shows that the 
Bloom Filter is faster than
B + Trees in all runs. This is due to the probabilistic nature of the structure , thus 
it lacks
accuracy. Instead, B + Tree is looking for
the word itself and therefore reaches its leaves with 100% accuracy, although losing in time complexity.
Some indicative run times are shown below:

|  # Files / File Size | Bloom Filter  |  B+ Tree |
|---|---|---|
|  319 / 1.31 MB|  0.28(s) |  0.81(s) |
|  392 / 1.12 MB | 0.12(s)  | 0.47(s) |
| 394 / 1.44 MB  | 0.28(s)  | 0.78(s)  |
|  399 / 1.28 MB | 0.31(s)  |  0.73(s) |
|  984 / 2.98 MB |  0.50(s) |  1.64(s) |

## LSH vs Cosine Similarity
* For the **Locality Sensitive Hashing (LSH)** approach, we used MinHash to 
implement it. It should be noted that the MinHash approach involves randomness 
and thus any execution of the program could
give different results.
Initially each document is represented as a set of
shingles. Then we use the MinHash algorithm for
the calculation of the signature vectors that represent
each document. These vectors can be compared
between them by calculating the number of items that
"agree"  in their data. Finally, we compare
pairs of documents, and we find those that have the
higher similarity.

* The **Cosine Similarity** method requires vectorizing the words in the document and then
calculating the vectors' similarity by measuring their inner product space.

* **The comparison** between the two document similarity measuring techniques 
concludes that although the cosine similarity method is very accurate, it is
much slower (O(n^2)) than LSH - MinHash
approach (O(n)).
The use of the upper triangular matrix and the nature of the LSH algorithm
helped reducing time and space complexity dramatically.
Some indicative run times are shown below:

|  # Files / File Size | Cosine Similarity  |  LSH |
|---|---|---|
|  578 / 0.69 MB|  146.32(s) |  0.48(s) |
|  319 / 0.70 MB | 148.67(s)  | 0.50(s) |
| 590 / 0.79 MB  | 161.23(s)  | 0.58(s)  |
|  584 / 0.90 MB | 178.57(s)  |  0.71(s) |
|  591 / 1.80 MB |  373.57(s) |  1.48(s) |

## How to run
* `preprocessing.py` is used before running the `LSH.py` , so the `data.txt` file is created.