from os.path import dirname


class Evaluation:

    def __init__(self):
        self.START_PATH = dirname(dirname(dirname(__file__))) + '/data/'
        self.REL_FILE = self.START_PATH + 'cacm.rel.txt'
        self.relevance_values = self.get_rel_values()

    def get_rel_values(self):
        all_relevance_values = dict()
        with open(self.REL_FILE, 'r') as f:
            lines = f.read().splitlines()
        f.close()
        for line in lines:
            words = line.split(' ')
            query_id = words[0]
            doc_id = words[-2]
            rel_list = all_relevance_values.get(query_id, set())
            rel_list.add(doc_id)
            all_relevance_values[query_id] = rel_list
        return all_relevance_values


def main():
    e = Evaluation()
    # print(e.relevance_values)


main()
