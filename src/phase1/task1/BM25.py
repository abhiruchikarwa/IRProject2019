from src.phase1 import Helper
from collections import OrderedDict
import math
import nltk
import os

QUERY_INPUT_FILE = 'queries.txt'
OUTPUT_FILE_PATH = 'BM25_results/'

## CONSTANTS (given in the assignment description)
k1 = 1.2
b = 0.75
k2 = 100


def average_length_of_docs(docs):
    sum = 0
    for v in docs.values():
        sum += v
    return sum/len(docs)

def get_BM25_score(N, ni, dl, K, fi, qfi):
    # N : total number of documents in the corpus
    # ni: total number of documents in which this term occurs
    # dl: the document length of the document under consideration
    # K : the value found for every document using formula  K = k1 * ((1 - b) + b * (dl/avdl))
    # fi: term frequency of the term under consideration in the document under consideration
    # qfi: frequency of the term in the query
    # ri = R = 0 as no relevance information is assumed
    # score = log (ri + 0.5)/(R − ri + 0.5)/(ni − ri + 0.5)/(N − ni − R + ri + 0.5) · (k1 + 1)fi / K + fi · (k2 + 1)qfi / k2 + qfi (source: Text book, Search Engines, information retrieval in practice)
    partial_score = math.log(1/((ni - 0.5)/(N - ni - 0.5))) * (k1 + 1) * fi * (1 / (K + fi)) * (k2 + 1) * qfi * (1/(k2 + qfi))
    return partial_score

def get_top_100_relevant_documents(inverted_index, query, avdl):
    # maintain a score list
    score_list = dict()
    document_term_count = h.document_term_count
    N = len(h.document_term_count)
    for term, freq in nltk.FreqDist(query.split()).items():  
        # for each term in the query fetch and traverse the inverted list
        if term not in inverted_index:
            continue
        inv_list = inverted_index[term]
        for posting in inv_list:
            dl = document_term_count[posting[0]]
            # calculate the value of K for this document 
            K = k1 * ((1 - b) + b * (dl/avdl))
            # calculate the score for a document for that term
            score = get_BM25_score(N, len(inv_list), dl, K, posting[1], freq)
            # update the score in the score list for every document in the inverted list for the corresponding term in the query
            if posting[0] in score_list:
                score_list[posting[0]] += score
            else:
                score_list[posting[0]] = score
    return OrderedDict(sorted(score_list.items(), key = lambda item: item[1], reverse = True)[:100]) # 100 for top-100 results only


query_id = 1

def process_query(query, inverted_index, avdl):
    global query_id
    # query = ' '.join(query.split(' ')[1:]).rstrip()
    # fetch top relevant results
    results = get_top_100_relevant_documents(inverted_index, query, avdl)
    # write the results to a file
    if not os.path.exists(OUTPUT_FILE_PATH):
        os.makedirs(OUTPUT_FILE_PATH)
    f_obj = open(OUTPUT_FILE_PATH + str(query_id) +'.txt', 'w', encoding='utf-8')
    rank = 1
    for docid, score in results.items():
        f_obj.write(str(query_id) + " Q0 " + docid + " " + str(rank)  + " " + str(score) + " BM25" + '\n')
        rank += 1
    f_obj.close()
    query_id += 1

def main():
    # generate index and the vocab counts

    inverted_index = h.get_inverted_index()
    # find the average length of docs in the index across the corpus.
    avdl = average_length_of_docs(h.document_term_count)
    # read queries
    for query in h.get_queries().values():
        process_query(query, inverted_index, avdl)
        
h = Helper.Helper()
if __name__ == "__main__":
    main()