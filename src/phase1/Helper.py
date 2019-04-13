from collections import defaultdict
from os import listdir
from os.path import isfile, join, dirname
import nltk
from bs4 import BeautifulSoup
import time 
import re
from nltk.tokenize import word_tokenize


class Helper:
    def __init__(self):
        self.ROOT_OUTPUT_FOLDER = dirname(dirname(dirname(__file__))) + "/clean_corpus/"
        self.ROOT_INPUT_FOLDER =  dirname(dirname(dirname(__file__))) + "/data/cacm/"
        self.total_number_of_terms_corpus = 0
        self.clean_dataset()
         # maintain a global inverted index
        self.inverted_index = dict()
        # maintain a map for document -> vocabulary count
        self.document_term_count = dict()
        self.generate_inverted_index()

    def generate_inverted_index(self):
        # fetch all file names
        files = [f for f in listdir(self.ROOT_OUTPUT_FOLDER) if isfile(join(self.ROOT_OUTPUT_FOLDER, f))]
        count = 0
        # iterate through the files
        for f in files:
            # fetch the doc id
            docID = f[:-4]
            count += 1
            # maintain a document-wide frequency distribution map
            freq_dist = nltk.FreqDist()
            f_obj = open(join(self.ROOT_OUTPUT_FOLDER, f),'rb')
            text = f_obj.read().decode('utf-8')
            # update the frequency distribution with the frequency distribution of unigrams in this document
            freq_dist.update(text.split())  # for uni-grams
            for ngram ,frequency in freq_dist.items():
                # add the ngram and a posting list for this document in the inverted index if not present
                if ngram not in self.inverted_index:
                    self.inverted_index[ngram] = [(docID, frequency)]
                # if ngram already present in the inverted index update the posting list with a posting for this document
                else:
                    posting_list = self.inverted_index[ngram]
                    posting_list.append((docID,frequency))
            if count == 1000:
                break
            #print(docID)
            # update the document vocabulary for this document in the map    
            self.document_term_count[docID] = len(text.split()) 
        out_put_file = open('../unigrams_inverted_index.txt', 'w', encoding='utf-8') # for uni-grams
        # write the inverted index into the output file
        for k, v in self.inverted_index.items():
            out_put_file.write(k + ":" + str(v) + "\n")
        doc_vocab_length_file = open('../terms_in_document.txt', 'w', encoding='utf-8')
        # write the document vocabulary map in a separate output file
        for k, v in self.document_term_count.items():
            doc_vocab_length_file.write(k + ":" + str(v) + "\n")

    def corpus_frequency(self, unigram_inverted_index):
        corpus_term_count_dictionary = {}
        for key1 in unigram_inverted_index.keys():
            corpus_term_count_dictionary[key1] = 0
            for key2 in unigram_inverted_index[key1].keys():
                corpus_term_count_dictionary[key1] += unigram_inverted_index[key1][key2]

        return corpus_term_count_dictionary

    def get_queries(self):
        queries = {}
        with open('../../data/cacm.query.txt', 'r') as f:
            raw_data = f.read()
            bs = BeautifulSoup(raw_data, 'html.parser')
            docs = bs.find_all('doc')
            for doc in docs:
                doc_text = doc.get_text()
                line = doc_text.replace("\n", '')
                line_list = line.split()
                query_id = int(line_list.pop(0))
                query = ' '.join(line_list)
                query = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", query)
                query = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", query, 0)
                queries[query_id] = query.lower()
        return queries
    def __crawl(self, f):
        f_obj = open(join(self.ROOT_INPUT_FOLDER, f), "r")
        bs_object = BeautifulSoup(f_obj.read(), "html.parser")
            
        # retrieve the content from the pre tags in the files
        content_block = bs_object.find('pre') 
        text = content_block.get_text()
        filtered_text =" ".join([re.sub('[^a-zA-Z0-9\s\r\n-]', '', word) for word in text.split()])
        output_file = open(self.ROOT_OUTPUT_FOLDER + f + ".txt", 'w')
        output_file.write(filtered_text)
        output_file.close()

    def clean_dataset(self):
        print("crawling... this might take some time!")
        start_time = time.time()
        files = [f for f in listdir(self.ROOT_INPUT_FOLDER) if isfile(join(self.ROOT_INPUT_FOLDER, f))]
        for f in files:
            self.__crawl(f)
        end_time = time.time()
        print("This crawl took " + str(end_time - start_time) + " seconds to complete")

def main():
    h = Helper()
    # queries = h.get_queries()
    # with open('../../data/queries.txt', 'w') as f:
    #     for key, value in queries.items():
    #         f.write(str(key) + ': ' + value + '\n')
    # f.close()

main()
