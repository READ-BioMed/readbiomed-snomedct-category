import logging
import json
import jsonpickle
from pymetamap import SubprocessBackend
import requests
from tqdm import tqdm
import urllib.parse


class Category():

    def normalise_pre_term(self, term):
        return term.lower().replace("-", " ")

    def get_predefined(self):
        with open('./data/direct_all_possible_reasons_and_synonyms.json', 'r') as f:
            predefined = json.load(f)

        return {self.normalise_pre_term(term): k for k, v in predefined.items() for term in v}

    def save_cache(self):
        with open('./data/cache.json', 'w') as f:
            json.dump(jsonpickle.encode(self.category_cache), f)


    def __init__(self, ontoserver_prefix="https://r4.ontoserver.csiro.au"):
        with open('./data/snomedct2path.json', 'r') as f:
            self.hp = jsonpickle.decode(json.load(f))
            self.predefined = self.get_predefined()
            self.ontoserver_prefix = ontoserver_prefix
        self.mm = SubprocessBackend("/metamap/public_mm/bin/metamap20")


        try:
            with open('./data/cache.json', 'r') as f:
                self.category_cache = jsonpickle.decode(json.load(f))
        except:
            logging.debug('Regenerating the cache')
            self.category_cache = {}

        self.onto_cache = {}

        logging.info("Resources loaded")

    def get_ids(self, term):
        logging.debug("Ontoserver: {}".format(term))

        if term in self.onto_cache:
            return self.onto_cache[term]
        ids = []

        answer = requests.request('GET', "{}/fhir/ConceptMap/$translate?url=http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-seq;automapstrategy-default;automapstrategy-MML&system=http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms&code={}&target=http://snomed.info/sct?fhir_vs".format(
            self.ontoserver_prefix, urllib.parse.quote(term))).json()

        logging.debug("Ontoserver answer {}".format(answer))

        try:
            for i in answer['parameter']:
                if i['name'] == 'match':
                    for c in i['part']:
                        if c['name'] == 'concept':
                            ids.append(c['valueCoding']['code'])
        except:
            logging.error('Error processing Ontoserver output')

        self.onto_cache[term] = ids
        return ids

    def get_terms(self, term):
        terms = []

        for s in self.mm.extract_concepts(sentences=[term], restrict_to_sources=["SNOMEDCT_US"]):
            if s is not None:
                for p in range(len(s)):
                    logging.debug("MetaMap term {} for {}".format(
                        s[p].preferred_name, term))
                    terms.append(s[p].preferred_name)

        return terms

    def get_category(self, term):
        logging.debug("Processing {}".format(term))

        if term in self.category_cache:
            return (term, self.category_cache[term])

        category = self.get_category_ontoserver(term)

        if category is None:
            for mterm in self.get_terms(term):
                category = self.get_category_ontoserver(mterm)

                if category is not None:
                    break

        self.category_cache[term] = category
        return (term, category)

    def get_category_ontoserver(self, term):
        try:
            term = str(term)

            if self.normalise_pre_term(term) in self.predefined:
                output = self.predefined[self.normalise_pre_term(term)]
                logging.debug("Found term {} in {}".format(
                    self.normalise_pre_term(term), output))
                return output

            ids = self.get_ids(term)

            for id in ids:
                if id in self.hp:
                    logging.debug("Id {} found {}".format(id, self.hp[id]))
                    if len(self.hp[id]) > 0 and self.hp[id] is not None:
                        return sorted(self.hp[id].items(), key=lambda x: x[1], reverse=True)
        except:
            logging.debug("Error processing {}".format(term))

        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    predict = Category("http://100.100.0.4:8080")

    for i in tqdm(range(100)):
        print(predict.get_category("File review"))
        print(predict.get_category("follow-up"))
        print(predict.get_category("follow up"))
        print(predict.get_category("FOLLOW UP"))
        print(predict.get_category('wound care'))
        print(predict.get_category('telephone consultation'))
        print(predict.get_category('18/12 immunisation'))
        print(predict.get_category('glaucoma'))
        print(predict.get_category('referral letter'))
        print(predict.get_category('asthma'))
