import json
import jsonpickle
import requests
from tqdm import tqdm


class Category():
    def get_predefined(self):
        with open('/Users/E114560/Documents/git/mcri-rfv/data/direct_all_possible_reasons_and_synonyms.json', 'r') as f:
            predefined = json.load(f)

        return {term.lower(): k for k, v in predefined.items() for term in v}

    def __init__(self, ontoserver_prefix="https://r4.ontoserver.csiro.au"):
        with open('./snomedct2path.json', 'r') as f:
            self.hp = jsonpickle.decode(json.load(f))
            self.predefined = self.get_predefined()
            self.ontoserver_prefix = ontoserver_prefix

        print("loaded")

    def get_ids(self, term):
        ids = []

        answer = requests.request('GET', "{}/fhir/ConceptMap/$translate?url=http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-seq;automapstrategy-default;automapstrategy-MML&system=http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms&code={}&target=http://snomed.info/sct?fhir_vs".format(self.ontoserver_prefix, term)).json()

        for i in answer['parameter']:
            if i['name'] == 'match':
                for c in i['part']:
                    if c['name'] == 'concept':
                        ids.append(c['valueCoding']['code'])

        return ids

    def get_category(self, term):
        if term.lower() in self.predefined:
            return self.predefined[term.lower()]

        ids = self.get_ids(term)

        for id in ids:
            if id in self.hp:
                if len(self.hp[id]) > 0:
                    return sorted(self.hp[id].items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    predict = Category()

    for i in tqdm(range(1)):
        print(predict.get_category('imaging'))
