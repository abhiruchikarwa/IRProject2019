import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.phase1 import Helper
import os


additional_query_terms = 8

h = Helper.Helper()
queries = list(h.get_queries().values())

newpath = "Query Expansion/"
if not os.path.exists(newpath):
    os.makedirs(newpath)

fout = open(newpath + "query_expanded_thesaurus.txt", "w", encoding="utf-8")
stop_words = set(stopwords.words("english"))

i = 1

for query in queries:
    query = query.lower()
    query=query.translate(str.maketrans('','',string.punctuation))
    word_tokens = word_tokenize(query)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    synonyms = []

    count = 0
    for x in filtered_sentence:

        for syn in wordnet.synsets(x):
            for l in syn.lemmas():
                if (count < 3):
                    if l.name() not in synonyms:
                        synonyms.append(l.name())
                        count += 1

        count = 0

    synonyms_string = ' '.join(synonyms[:additional_query_terms] + filtered_sentence)
    synonyms = []
    fout.write("Query: " + str(i) + "  Terms: " + synonyms_string)
    fout.write('\n')
    i += 1

fout.close()

