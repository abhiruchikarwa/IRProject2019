import math
import operator

from src.phase1 import Helper
from collections import defaultdict


class JMRetriever:
    def __init__(self):
        self.helper = Helper.Helper()
        self.inverted_index = self.helper.get_inverted_index()
        self.corpus_term_count = self.helper.corpus_frequency()
        self.lambda_value = 0.35
        self.number_of_ranked_docs = 100
        self.output_folder = 'JM_QLM_results/'

    def run(self, query, query_id):
        query = self.helper.parse_query(query)
        terms = query.split()
        doc_scores = defaultdict(float)
        for term in terms:
            if term in self.inverted_index.keys():
                posting_list = self.inverted_index[term]
                for posting in posting_list:
                    doc_id = posting[0]
                    doc_scores[doc_id] += self.calculate_document_score(doc_id, term)

            sorted_scores = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)
            self.save_results(query_id, sorted_scores)

    def save_results(self, query_id, scored_docs):
        count = 1
        file_name = self.output_folder + str(query_id) + '.txt'
        
        with open(file_name, 'w') as f:
            for doc in scored_docs:
                doc_name = doc[0].upper() + '.html'
                if count <= 100:
                    f.write(str(query_id) + " Q0 " + doc_name + " " + str(count) + " " + str(doc[1]) +
                            " JM_Smoothed_Query_Likelihood_Model\n")
                    count += 1
                else:
                    break

    def calculate_document_score(self, doc_id, term):
        # fqi, D
        term_df = self.get_term_df(term, doc_id)

        # |D|
        doc_term_count = self.helper.document_term_count[doc_id] * 1.0

        # Cqi
        total_term_frequency = self.corpus_term_count[term] * 1.0

        # |C|
        # total_term_count = self.helper.total_number_of_terms_corpus * 1.0
        total_term_count = len(self.inverted_index) * 1.0

        lm_probability = ((1 - self.lambda_value) * (term_df / doc_term_count))
        cm_probability = (self.lambda_value * (total_term_frequency / total_term_count))
        return math.log(lm_probability + cm_probability)

    def get_term_df(self, term, doc_id):
        posting_list = self.inverted_index[term]
        for posting in posting_list:
            if doc_id == posting[0]:
                return posting[1] * 1.0
        return 0.0

    def main(self):
        queries = self.helper.get_queries()
        for query_id, query in queries.items():
            self.run(query, query_id)


def main():
    j = JMRetriever()
    j.main()


main()
