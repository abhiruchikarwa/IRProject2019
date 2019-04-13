from src.phase1 import Helper
import math
from collections import defaultdict
import operator
import os
import collections
import pickle
#
# class TfIdf:
# 	def __init__(self):
# 		self.dfDict = defaultdict(int)
# 		self.tfIdfDict = defaultdict(dict)
# 		self.idfDict = defaultdict(float)
# 		self.number_of_documents = len(r.document_term_count.keys())
# 		# self.printTF()
# 		# self.calculateDocumentFrequency()
# 		# self.calculateInverseDocumentFrequency()
# 		# self.calculateTFIdfScore()
# 		# self.writeTfIdfScoreToFile()
# 		self.inverted_index = r.get_inverted_index()
# 		# self.performQueryTfIdf()
# 		self.performTfIDfForQuery()
#
#
# 	def performTfIDfForQuery(self):
# 		f = open('TF_IDF_Normalized_Top100_Pages.txt', 'w')
#
# 		f.write('Ranking (Top 100) for the queries in Cleaned_Queries.txt in the format:' + "\n")
# 		f.write('query_id Q0 doc_id rank TF-IDF_normalized_score system_name' + "\n\n")
# 		i = 0
# 		for query in r.get_queries().values():
# 			c = 1  # the variable c denotes rank
# 			print("Calculating TF-IDF Normalized Score for query: " + str(query))
# 			tf_idf_score = self.calc_score(query)
# 			final_score1 = collections.OrderedDict(sorted(tf_idf_score.items(), key=lambda s: s[1], reverse=True))
# 			f.write('\nFor query : %s\n\n' % query)
# 			for quid in final_score1:
# 				if c < 100:
# 					# format-> query_id Q0 doc_id rank BM25_score system_name
# 					f.write('%d Q0 %s %d %s tf_idf_model\n' % (i, quid, c, final_score1[quid]))
# 				c += 1
# 			newpath = r'../../Encoded Data Structures/Encoded-TF-IDF-Normalized-Top100Docs-perQuery/'
# 			if not os.path.exists(newpath):
# 				os.makedirs(newpath)
# 			output = open(
# 				newpath + 'Encoded-Top100Docs-TF-IDF-Normalized' + '_%d' % i + '.txt', 'wb')
# 			pickle.dump(final_score1, output)
# 			output.close()
# 			i += 1
# 		f.close()
#
# 	def printTF(self):
# 		for entry in r.inverted_index:
# 			for en in r.inverted_index[entry]:
# 				print(entry)
# 				print(en)
# 				print(r.inverted_index[entry][en])
# 		# number_terms_doc
#
# 	def calculateDocumentFrequency(self):
# 		for term in r.inverted_index:
# 			self.dfDict[term] = len(r.inverted_index[term].keys()+1)
#
# 			# print term
# 			# print self.dfDict[term]
#
# 	def calculateInverseDocumentFrequency(self):
# 		for term in self.dfDict:
# 			self.idfDict[term] = 1.0 + math.log(float(self.number_of_documents)/float(self.dfDict[term]))
# 			# print term
# 			# print self.idfDict[term]
#
# 	def calculateTFIdfScore(self,doc_id,term):
# 		# for term in r.unigram_inverted_index:
# 		# 	for doc_id in r.unigram_inverted_index[term]:
# 		if term in r.inverted_index.keys():
# 			values = defaultdict(int)
# 			values = r.inverted_index[term]
# 			if doc_id in values.keys():
# 				return (float(r.inverted_index[term][doc_id])/float(r.document_term_count[doc_id])) * self.idfDict[term]
# 			else:
# 				return 0
# 		# print self.tfIdfDict
#
# 		# self.tfIdfDict = sorted(self.tfIdfDict.items(), key=operator.itemgetter(1))
# 		# print self.tfIdfDict
#
# 	def writeTfIdfScoreToFile(self,query,queryId,sorted_scores):
# 		count = 1
# 		file_name = 'TF-IDF_output/' + str(queryId) + '.txt'
# 		print ('writing' + str(queryId))
#
# 		with open(file_name, 'w') as f:
# 			for word in sorted_scores:
# 				if count <= 100:
# 					f.write(str(queryId))
# 					f.write(" ")
# 					f.write("Q0")
# 					f.write(" ")
# 					f.write(word[0])
# 					f.write(" ")
# 					f.write(str(count))
# 					f.write(" ")
# 					f.write(str(word[1]))
# 					f.write(" ")
# 					f.write("TF-IDF_Unigram_Casefolding_PunctuationHandling")
# 					f.write("\n")
# 					count += 1
# 				else:
# 					break
#
# 	def getTfIdf(self, queryTF, inverted_list, queryId, query):
# 		documentScores = defaultdict()
# 		tfIdf = defaultdict()
#
# 		for term in inverted_list:
# 			idf = 1.0+ math.log(float(self.number_of_documents) / float(len(inverted_list[term].keys())+1))
# 			for docId in inverted_list[term]:
# 				tf = float(inverted_list[term][docId])/float(r.document_term_count[docId])
# 				if term not in tfIdf:
# 					tfIdf[term] = {}
# 				tfIdf[term][docId] = tf*idf
#
# 		for term in inverted_list:
# 			for document in inverted_list[term]:
# 				docWeight = 0
# 				docWeight+= tfIdf[term][document]
# 				if document in documentScores:
# 					docWeight += documentScores[document]
# 				documentScores.update({document:docWeight})
#
# 		self.sort_scores(query,queryId,documentScores)
#
# 	def sort_scores(self, query, query_id, doc_scores):
# 		sorted_scores = sorted(
# 			doc_scores.items(), key=operator.itemgetter(1), reverse=True)
# 		self.writeTfIdfScoreToFile(query, query_id, sorted_scores)
#
# 	def getQueryTermFrequency(self,query):
# 		query_tf = defaultdict(int)
# 		for term in query.split():
# 			if term not in query_tf:
# 				query_tf[term] += 1
# 		return query_tf
#
# 	def getDocumentsContainingTerm(self,queryTF):
# 		documents_containing_term = defaultdict()
# 		for term in queryTF:
# 			documents_containing_term[term] = r.inverted_index[term]
#
# 		return documents_containing_term
#
# 	def tf_idf(self, tf, df, d):
#
# 		n = len(r.document_term_count.keys())
# 		idf = math.log(n / df + 1) + 1
# 		normalized_tf = tf / d
# 		score = normalized_tf * idf
#
# 		return score
#
# 	def calc_score(self, q):
# 		final_score = {}
# 		terms = q.split()
# 		for term in terms:
# 			if term in self.inverted_index:
# 				for doc in self, self.inverted_index[term]:
# 					print("Doc")
# 					print(doc)
# 					if doc[0] not in final_score.keys():
# 						final_score[doc[0]] = self.tf_idf(doc[1], len(self.inverted_index[term]), r.document_term_count[doc[0]])
# 					else:
# 						final_score[doc[0]] += self.tf_idf(doc[1], len(self.inverted_index[term]), r.document_term_count[doc[0]])
#
# 		return final_score
#
#
# 	def performQueryTfIdf(self):
# 		self.queries = r.get_queries()
# 		for query in self.queries:
# 			self.queries[query] = r.parse_query(self.queries[query])
# 			self.queryTF = self.getQueryTermFrequency(self.queries[query])
# 			self.inverted_list = self.getDocumentsContainingTerm(self.queryTF)
# 			self.getTfIdf(self.queryTF, self.inverted_list, query, self.queries[query])
# 			# self.getTfIdf (self.queries[query],query)
#
# 		# for query in self.queries:
# 		# 	self.getTfIdf (self.queries[query],query)
#
#
r = Helper.Helper()

import pickle
import math
import collections
import os

# This script implements the TF-IDF Model for ranking the documents for every query
# and retrieving the top 100 documents from the ranked documents

# Access Encoded Data Structures
inverted_index = r.get_inverted_index()

docID_documentLen = r.document_term_count

query_dict = r.get_queries()

query_list = list(query_dict.values())    # Contains all the queries required

# idf = log(N/df)

final_score = {}     # dictionary of docID, bm25-score


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
    print(i)
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

print("\n\nTF-IDF Scoring Process DONE")
