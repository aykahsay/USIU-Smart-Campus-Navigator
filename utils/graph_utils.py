# graph_utils.py

import networkx as nx
from math import sqrt
import json

def euclidean(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def load_graph_from_json(file_path):
    with open(file_path) as f:
        data = json.load(f)

    G = nx.Graph()
    for edge in data["features"]:
        props = edge["properties"]
        coords = edge["geometry"]["coordinates"]

        start = props["start_name"]
        end = props["end_name"]
        route_name = props["route_name"]
        start_coord = tuple(coords[0])
        end_coord = tuple(coords[-1])

        G.add_node(start, coord=start_coord)
        G.add_node(end, coord=end_coord)

        G.add_edge(start, end,
                   weight=euclidean(start_coord, end_coord),
                   geometry=coords,
                   name=route_name)
    return G
