import json
from tqdm import tqdm

# Create a concept catalogue for SNOMED CT with their correspinding CUI
if __name__ == '__main__':
    dinv = {}
    # https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/
    with open('/Users/E114560/Downloads/MRCONSO.RRF', 'r') as f:
        for l in tqdm(f.readlines()):
            tokens = l.split("|")

            if tokens[11] == "SNOMEDCT_US":
                dinv[tokens[13]] = tokens[0]

    with open('./snomedct2cui.json', 'w') as f:
        json.dump(dinv, f)