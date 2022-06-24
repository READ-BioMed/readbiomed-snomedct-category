import json
import jsonpickle
import requests
from tqdm import tqdm

with open('./snomedct2path.json', 'r') as f:
    hp = jsonpickle.decode(json.load(f))

print("loaded")


def get_ids(term):
    ids = []

    answer = requests.request('GET', "https://r4.ontoserver.csiro.au/fhir/ConceptMap/$translate?url=http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-default&system=http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms&code={}&target=http://snomed.info/sct?fhir_vs".format(term)).json()

    for i in answer['parameter']:
        if i['name'] == 'match':
            for c in i['part']:
                if c['name'] == 'concept':
                    ids.append(c['valueCoding']['code'])

    return ids


def get_category(term):
    ids = get_ids(term)

    for id in ids:
        if id in hp:
            if len(hp[id]) > 0:
                return sorted(hp[id].items(), key=lambda x: x[1], reverse=True)[0]


for i in tqdm(range(1)):
    print(get_category('flu'))
