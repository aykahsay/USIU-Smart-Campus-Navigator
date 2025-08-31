from flask import Flask, render_template, request, redirect, url_for, session
import geopandas as gpd
import networkx as nx
from math import sqrt
import folium
import os
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for session management

# === Load Graph ===
gdf = gpd.read_file("data/combined_cleaned_routes.geojson")
G = nx.Graph()

disabled_path = "data/disabled_routes.json"
if os.path.exists(disabled_path):
    with open(disabled_path, "r") as f:
        DISABLED_EDGES = set(tuple(edge) for edge in json.load(f).get("disabled_edges", []))
else:
    DISABLED_EDGES = set()

for _, row in gdf.iterrows():
    start = row["start_name"]
    end = row["end_name"]
    coords = list(row.geometry.coords)
    if len(coords) < 2:
        continue
    G.add_node(start, pos=coords[0])
    G.add_node(end, pos=coords[-1])
    G.add_edge(start, end,
               weight=row.geometry.length,
               geometry=row.geometry,
               route_name=row.get("route_name", "Unnamed Route"),
               route_type=row.get("route_type", "unknown"),
               wheelchair_accessible=row.get("wheelchair_accessible", True))

# === Heuristic ===
def euclidean_heuristic(u, v):
    ux, uy = G.nodes[u]["pos"]
    vx, vy = G.nodes[v]["pos"]
    return sqrt((ux - vx)**2 + (uy - vy)**2)

# === Folium Map ===
def create_folium_map(route_nodes, G_used):
    if not os.path.exists("static"):
        os.makedirs("static")
    center = G_used.nodes[route_nodes[0]]["pos"]
    fmap = folium.Map(location=[center[1], center[0]], zoom_start=17)

    for u, v, data in G_used.edges(data=True):
        geom = data.get("geometry")
        if geom:
            coords = [(pt[1], pt[0]) for pt in geom.coords]
            color = "blue" if data.get("route_type") == "car" else "green"
            folium.PolyLine(coords, color=color, weight=2, opacity=0.4).add_to(fmap)

    for node in route_nodes:
        lat, lon = G_used.nodes[node]["pos"][1], G_used.nodes[node]["pos"][0]
        folium.Marker([lat, lon], tooltip=node, icon=folium.Icon(color="blue")).add_to(fmap)

    for i in range(len(route_nodes) - 1):
        u, v = route_nodes[i], route_nodes[i + 1]
        if G_used.has_edge(u, v):
            coords = [(pt[1], pt[0]) for pt in G_used[u][v]["geometry"].coords]
            folium.PolyLine(coords, color="red", weight=5).add_to(fmap)

    fmap.save("static/route_map.html")

# === User Route ===
@app.route("/", methods=["GET", "POST"])
def index():
    nodes = sorted(G.nodes)
    route = []
    total_distance = None
    error = None

    if request.method == "POST":
        start = request.form.get("start")
        end = request.form.get("end")
        mode = request.form.get("mode", "any")
        wheelchair = request.form.get("wheelchair") == "on"
        intermediates = [i for i in request.form.getlist("intermediates") if i and i not in [start, end]]

        if not start or not end:
            error = "❌ Start and end points are required."
        else:
            G_active = nx.Graph()
            for u, v, data in G.edges(data=True):
                if (u, v) in DISABLED_EDGES or (v, u) in DISABLED_EDGES:
                    continue
                if wheelchair and not data.get("wheelchair_accessible", True):
                    continue
                if mode != "any" and data.get("route_type") != mode:
                    continue
                G_active.add_edge(u, v, **data)
                G_active.add_node(u, pos=G.nodes[u]["pos"])
                G_active.add_node(v, pos=G.nodes[v]["pos"])

            try:
                all_points = [start] + intermediates + [end]
                full_route = []
                total_distance = 0
                for i in range(len(all_points)-1):
                    segment = nx.astar_path(G_active, all_points[i], all_points[i+1],
                                            heuristic=euclidean_heuristic, weight="weight")
                    if full_route:
                        full_route.extend(segment[1:])
                    else:
                        full_route.extend(segment)
                    total_distance += sum(
                        G_active[segment[j]][segment[j+1]]["weight"] for j in range(len(segment)-1)
                    )
                route = full_route
                create_folium_map(route, G_active)
            except nx.NetworkXNoPath:
                error = "❌ No accessible path found between some points."

    return render_template("index.html", nodes=nodes, route=route,
                           total_distance=round(total_distance*111139,2) if total_distance else None,
                           error=error)

# === Admin Login ===
ADMIN_PASSWORD = "admin123"  # replace with your secure password

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error = "❌ Incorrect password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))

# === Admin Route ===
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    edges_display = sorted([(u,v) for u,v in G.edges if u<=v])
    error = None
    success = None

    if request.method == "POST":
        form_data = request.form.getlist("disabled")
        new_disabled = set(tuple(edge.split("|||")) for edge in form_data)
        try:
            with open(disabled_path, "w") as f:
                json.dump({"disabled_edges": list(new_disabled)}, f, indent=2)
            global DISABLED_EDGES
            DISABLED_EDGES = new_disabled
            success = "✅ Disabled edges updated successfully."
        except Exception as e:
            error = f"❌ Failed to save changes: {e}"

    return render_template("admin.html", edges=edges_display,
                           disabled_edges=DISABLED_EDGES,
                           error=error, success=success)
