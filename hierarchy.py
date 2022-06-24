import json
import jsonpickle
from tqdm import tqdm

d = {}

# https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.related_concepts_file_mrrel_rrf/
with open('/Users/E114560/Downloads/MRREL.RRF', 'r') as f:
    for l in tqdm(f.readlines()):
        tokens = l.split("|")

        if tokens[10] == "SNOMEDCT_US":
            if tokens[7] == 'isa':
                if tokens[4] not in d:
                    d[tokens[4]] = set()

                d[tokens[4]].add(tokens[0])

with open('./snomedct2hierarchy.json', 'w') as f:
    json.dump(jsonpickle.encode(d), f)