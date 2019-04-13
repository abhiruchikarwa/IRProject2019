from src.phase1 import Helper
import math
import collections
import os

r = Helper.Helper()


# This script implements the TF-IDF Model for ranking the documents for every query
# and retrieving the top 100 documents from the ranked documents

# Access Encoded Data Structures
inverted_index = r.get_inverted_index()
docID_documentLen = r.document_term_count
query_dict = r.get_queries()
query_list = list(query_dict.values())    # Contains all the queries required

# idf = log(N/df)

# dictionary of docID, bm25-score
final_score = {}


# # this function implements by calculating and returning a score
# based on the given arguments
def tf_idf(tf, df, D):

    N = len(docID_documentLen.keys())
    idf = math.log(N/df+1) + 1
    normalized_tf = tf/D
    score = normalized_tf * idf

    return score


# this function is used calculate the score for every document and calls the tf-idf function
def calc_score(q):
    final_score = {}
    terms = q.split()
    for term in terms:
        if term in inverted_index:
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = tf_idf(doc[1],len(inverted_index[term]), docID_documentLen[doc[0]])
                else:
                    final_score[doc[0]] += tf_idf(doc[1],len(inverted_index[term]), docID_documentLen[doc[0]])

    return final_score



def print_in_file(all_files, output):
    for file in all_files:
        output.write(file + ": " + str(all_files[file]) + "\n")

i = 1
for query in query_list:
    # the variable c denotes rank
    # print("Calculating TF-IDF Normalized Score for query: " + query)
    tf_idf_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(tf_idf_score.items(), key=lambda s: s[1], reverse=True)[:100])
    newpath = r'TF_IDF/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    output = open(
        newpath + str(i) + '.txt', 'w')

    srno = 1
    for file in final_score1:
        output.write(str(i) + " Q0 " + file + " " + str(srno) + " " + str(final_score1[file]) + " TF_IDF" +"\n")
        srno += 1
    output.close()
    i += 1
