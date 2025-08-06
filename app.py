from flask import Flask, render_template, request
import geopandas as gpd
import networkx as nx
from math import sqrt
import folium
from shapely.geometry import LineString
import os

app = Flask(__name__)

# === Load GeoJSON ===
gdf = gpd.read_file("data/combined_cleaned_routes.geojson")
G = nx.Graph()

# === Build Base Graph ===
for _, row in gdf.iterrows():
    start = row["start_name"]
    end = row["end_name"]
    coords = list(row.geometry.coords)
    start_coord = coords[0]
    end_coord = coords[-1]

    # Add nodes with positions
    G.add_node(start, pos=start_coord)
    G.add_node(end, pos=end_coord)

    # Add edge with attributes
    G.add_edge(start, end,
               weight=row.geometry.length,
               geometry=row.geometry,
               route_name=row.get("route_name", "Unnamed Route"),
               route_type=row.get("type", "unknown"),
               wheelchair_accessible=row.get("wheelchair_accessible", True))

# === Euclidean Distance Heuristic ===
def euclidean_heuristic(u, v):
    ux, uy = G.nodes[u]["pos"]
    vx, vy = G.nodes[v]["pos"]
    return sqrt((ux - vx)**2 + (uy - vy)**2)

# === Folium Map Generator ===
def create_folium_map(route_nodes, G_used):
    if not os.path.exists("static"):
        os.makedirs("static")

    # Center map at first point
    center = G_used.nodes[route_nodes[0]]["pos"]
    fmap = folium.Map(location=[center[1], center[0]], zoom_start=17)

    # Add markers
    for node in route_nodes:
        lat, lon = G_used.nodes[node]['pos'][1], G_used.nodes[node]['pos'][0]
        folium.Marker([lat, lon], tooltip=node, icon=folium.Icon(color="blue")).add_to(fmap)

    # Add route line
    route_coords = []
    for i in range(len(route_nodes) - 1):
        u, v = route_nodes[i], route_nodes[i + 1]
        if G_used.has_edge(u, v):
            geom = G_used[u][v].get("geometry")
            if geom:
                coords = [(pt[1], pt[0]) for pt in geom.coords]  # (lat, lon)
                route_coords.extend(coords)

    if route_coords:
        folium.PolyLine(route_coords, color="red", weight=5).add_to(fmap)

    # Save to static folder
    map_path = "static/route_map.html"
    fmap.save(map_path)

# === Flask Main Route ===
@app.route("/", methods=["GET", "POST"])
def index():
    nodes = sorted(G.nodes)
    route = []
    error = None
    total_distance = None

    if request.method == "POST":
        start = request.form["start"]
        end = request.form["end"]
        mode = request.form.get("mode", "any")  # any, pedestrian, car
        wheelchair = request.form.get("wheelchair") == "on"

        # Build filtered graph
        G_active = nx.Graph()
        for u, v, data in G.edges(data=True):
            if wheelchair and not data.get("wheelchair_accessible", True):
                continue
            if mode != "any" and data.get("route_type") != mode:
                continue
            G_active.add_edge(u, v, **data)
            G_active.add_node(u, pos=G.nodes[u]["pos"])
            G_active.add_node(v, pos=G.nodes[v]["pos"])

        # Compute shortest path
        if nx.has_path(G_active, start, end):
            route = nx.astar_path(G_active, source=start, target=end,
                                  heuristic=euclidean_heuristic, weight="weight")

            # Calculate total distance
            total_distance = 0
            for i in range(len(route) - 1):
                u, v = route[i], route[i + 1]
                if G_active.has_edge(u, v):
                    total_distance += G_active[u][v]["weight"]

            # Generate map
            create_folium_map(route, G_active)
        else:
            error = "❌ No accessible path found with selected options."

    return render_template("index.html",
                           nodes=nodes,
                           route=route,
                           total_distance=round(total_distance, 2) if total_distance else None,
                           error=error)

# === Run App ===
if __name__ == "__main__":
    app.run(debug=True)
