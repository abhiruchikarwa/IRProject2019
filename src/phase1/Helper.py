from collections import defaultdict
from os.path import join, dirname
from bs4 import BeautifulSoup

import re
import os
import nltk


class Helper:

    def __init__(self):
        self.start_path = dirname(dirname(dirname(__file__))) + '/data/'
        self.clean_corpus_dir = self.start_path + 'clean_corpus/'
        self.unigrams_file = self.start_path + 'unigrams_inverted_index.txt'
        self.term_count_file = self.start_path + 'terms_in_document.txt'
        self.raw_queries_file = self.start_path + 'cacm.query.txt'
        self.parsed_queries_file = self.start_path + 'queries.txt'

        self.queries = dict()
        self.total_number_of_terms_corpus = 0
        # maintain a global inverted index
        self.inverted_index = dict()
        # maintain a map for document -> vocabulary count
        self.document_term_count = dict()
        self.parse_queries()
        self.generate_inverted_index()

    def generate_inverted_index(self):
        # iterate through the files
        for f in os.listdir(self.clean_corpus_dir):
            doc_name = f[:-4]

            with open(join(self.clean_corpus_dir, f), 'rb') as clean_file:
                text = clean_file.read().decode('utf-8')
            clean_file.close()

            # maintain a document-wide frequency distribution map
            freq_dist = nltk.FreqDist()
            # update the frequency distribution with the frequency distribution of unigrams in this document
            freq_dist.update(text.split())  # for uni-grams
            for ngram, frequency in freq_dist.items():
                # add the ngram and a posting list for this document in the inverted index if not present
                if ngram not in self.inverted_index:
                    self.inverted_index[ngram] = [(doc_name, frequency)]
                else:
                    posting_list = self.inverted_index[ngram]
                    posting_list.append((doc_name, frequency))

            # update the document vocabulary for this document in the map
            number_of_terms = len(text.split())
            self.document_term_count[doc_name] = number_of_terms
            self.total_number_of_terms_corpus += number_of_terms
        # for uni-grams
        with open(self.unigrams_file, 'w', encoding='utf-8') as unigram_output:
            for k, v in self.inverted_index.items():
                unigram_output.write(k + ":" + str(v) + "\n")
        unigram_output.close()

        # for term-count
        with open(self.term_count_file, 'w', encoding='utf-8') as term_count_output:
            for k, v in self.document_term_count.items():
                term_count_output.write(k + ":" + str(v) + "\n")
        term_count_output.close()

    def corpus_frequency(self):
        corpus_term_count = dict()
        for term, postings in self.inverted_index.items():
            corpus_term_count[term] = 0
            for posting in postings:
                corpus_term_count[term] += posting[1]
        return corpus_term_count

    def parse_queries(self):
        queries = defaultdict()
        with open(self.raw_queries_file, 'r') as f:
            raw_data = f.read()
            bs = BeautifulSoup(raw_data, 'html.parser')
            docs = bs.find_all('doc')
            for doc in docs:
                line_list = doc.get_text().replace("\n", '').split()
                query_id = int(line_list.pop(0))
                query = ' '.join(line_list)
                queries[query_id] = self.parse_query(query)

        with open(self.parsed_queries_file, 'w') as f:
            for key, value in queries.items():
                f.write(str(key) + ' ' + value + '\n')
        f.close()
        self.queries = queries

    def parse_query(self, query):
        query = query.lower()
        regex = r"(?!\d)[.,;](?!\d)"
        regex2 = r"[(){}\"#~\[\]<>=:?!@&'|*]"
        regex3 = r"(?!\d|\w)[-/$](?!\d|\w)"
        query = re.sub(regex, "", query, 0)
        query = re.sub(regex2, "", query, 0)
        query = re.sub(regex3, "", query, 0)
        return query

    def get_inverted_index(self):
        return self.inverted_index

    def get_queries(self):
        return self.queries


class Preprocessor:
    def __init__(self):
        self.start_path = dirname(dirname(dirname(__file__))) + '/data/'
        self.raw_corpus_dir = self.start_path + 'cacm/'
        self.clean_corpus_dir = self.start_path + 'clean_corpus/'
        self.text_data = ''

    def clean_and_save(self):
        for file in os.listdir(self.raw_corpus_dir):
            file_path = self.raw_corpus_dir + file
            with open(file_path, 'r+') as f:
                raw_data = f.read()
            f.close()
            bs = BeautifulSoup(raw_data, 'html.parser')
            self.text_data = ''
            pre = bs.find('pre')
            self.text_data = pre.get_text()
            self.remove_punctuation_in_data()

            if ' PM' in self.text_data:
                self.text_data = self.text_data.split(' PM')[0] + ' PM'
            elif ' AM' in self.text_data:
                self.text_data = self.text_data.split(' AM')[0] + ' AM'

            # store data
            self.save_clean_file(file)

    def remove_punctuation_in_data(self):
        regex = r"(?!\d)[.,:;](?!\d)"
        regex2 = r"[(){}\"#~\[\]<>=?!@&'|*]"
        regex3 = r"(?!\d|\w)[-/$](?!\d|\w)"
        self.text_data = re.sub(regex, "", self.text_data, 0)
        self.text_data = re.sub(regex2, "", self.text_data, 0)
        self.text_data = re.sub(regex3, "", self.text_data, 0)

    def save_clean_file(self, file_name):
        file_name = file_name.replace('html', 'txt')
        file_name = (self.clean_corpus_dir + file_name).lower()
        with open(file_name, 'w') as f:
            f.write(self.text_data.lower())
        f.close()


def main():
    h = Helper()


main()
