# app.py

from flask import Flask, render_template, request
from graph_utils import load_graph_from_json
import networkx as nx
import folium
import os

app = Flask(__name__)

# Load graphs once
car_graph = load_graph_from_json("car_routes.json")
ped_graph = load_graph_from_json("pedestrian_routes.json")

@app.route("/", methods=["GET", "POST"])
def index():
    locations = sorted(set(car_graph.nodes) | set(ped_graph.nodes))

    if request.method == "POST":
        mode = request.form.get("mode")
        start = request.form.get("start")
        end = request.form.get("end")

        G = car_graph if mode == "car" else ped_graph

        if start not in G or end not in G or not nx.has_path(G, start, end):
            return render_template("result.html", error="Invalid or unreachable locations.")

        path = nx.shortest_path(G, start, end, weight="weight")
        coords = G.nodes[start]["coord"]
        m = folium.Map(location=[coords[1], coords[0]], zoom_start=18)

        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            line_coords = G[u][v]["geometry"]
            folium.PolyLine(locations=[(y, x) for x, y in line_coords], color="blue", weight=5).add_to(m)
            folium.Marker(location=(G.nodes[u]["coord"][1], G.nodes[u]["coord"][0]), tooltip=u,
                          icon=folium.Icon(color="green")).add_to(m)

        folium.Marker(location=(G.nodes[end]["coord"][1], G.nodes[end]["coord"][0]), tooltip=end,
                      icon=folium.Icon(color="red")).add_to(m)

        map_path = os.path.join("static", "route_map.html")
        m.save(map_path)

        return render_template("result.html", path=path, map_file=map_path)

    return render_template("index.html", locations=locations)

if __name__ == "__main__":
    app.run(debug=True)
