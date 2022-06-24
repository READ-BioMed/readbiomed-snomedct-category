import json
import jsonpickle
from tqdm import tqdm

# Identify the closest ancestor from a set of candidates
with open('./snomedct2cui.json', 'r') as f:
    c = json.load(f)

with open('../mcri-rfv/data/direct_main_codes.json', 'r') as f:
    codes = json.load(f)

categories = {}

for k, v in codes.items():
    categories[k] = []

    for sn in v:
        if sn not in c:
            print("SNOMEDCT code '{}' not found in UMLS.".format(sn))
        else:
            categories[k].append(c[sn])


with open('./snomedct2hierarchy.json', 'r') as f:
    h = jsonpickle.decode(json.load(f))


# https://onestepcode.com/graph-shortest-path-python/?utm_source=rss&utm_medium=rss&utm_campaign=graph-shortest-path-python
def shortest_path(node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]

        if last_node in h:
            next_nodes = h[last_node]
            # Search goal node
            if node2 in next_nodes:
                current_path.append(node2)
                return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes:
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    # To avoid backtracking
                    previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


concept2closest = {}

count = 0

for k, v in tqdm(c.items()):
    concept2closest[k] = {}

    for k1, v1 in categories.items():
        path_length = -1
        for code in v1:
            path = shortest_path(v, code)

            if path_length == -1:
                if len(path) > 0:
                    path_length = len(path)
            else:
                if len(path) > 0:
                    if len(path) < path_length:
                        path_length = len(path)

        if path_length > 0:
            concept2closest[k][k1] = path_length

with open('./snomedct2path.json', 'w') as f:
    json.dump(jsonpickle.encode(concept2closest), f)
