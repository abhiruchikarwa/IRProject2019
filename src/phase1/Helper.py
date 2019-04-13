from bs4 import BeautifulSoup
import re


class Helper:

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


def main():
    h = Helper()
    h.get_queries()


main()
