import geopandas as gpd
import networkx as nx
import folium
from math import sqrt
import webbrowser

def euclidean(a, b):
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def build_graph(gdf):
    G = nx.Graph()
    for _, row in gdf.iterrows():
        start = row["start_name"]
        end = row["end_name"]
        coords = list(row.geometry.coords)
        start_coord = coords[0]
        end_coord = coords[-1]

        G.add_node(start, coord=start_coord)
        G.add_node(end, coord=end_coord)

        G.add_edge(start, end,
                   weight=euclidean(start_coord, end_coord),
                   geometry=row.geometry,
                   name=row["route_name"])
    return G

def main():
    # Load routes
    print("Loading car routes...")
    car_gdf = gpd.read_file("combined_car_routes_named.geojson")

    print("Loading pedestrian routes...")
    ped_gdf = gpd.read_file("combined_pedestrian_routes_named.geojson")

    # Select mode
    mode = ""
    while mode not in ["car", "pedestrian"]:
        mode = input("Select mode (car/pedestrian): ").strip().lower()

    gdf = car_gdf if mode == "car" else ped_gdf

    # Build graph
    print(f"Building graph for {mode} routes...")
    G = build_graph(gdf)

    # Show locations
    print("\nAvailable locations:")
    for node in sorted(G.nodes):
        print(f" - {node}")

    # Input start and end
    start = input("\nEnter START location: ").strip()
    end = input("Enter END location: ").strip()

    if start not in G or end not in G:
        print("Invalid location name(s). Exiting.")
        return

    if not nx.has_path(G, start, end):
        print("No path found between these locations. Exiting.")
        return

    path = nx.shortest_path(G, start, end, weight="weight")
    print("\nShortest path:")
    for i, p in enumerate(path):
        print(f"{i+1}. {p}")

    # Generate map
    m = folium.Map(location=[G.nodes[start]['coord'][1], G.nodes[start]['coord'][0]], zoom_start=18)

    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        geom = G[u][v]["geometry"]
        folium.PolyLine(locations=[(y, x) for x, y in geom.coords], color="blue", weight=5).add_to(m)
        folium.Marker(location=(G.nodes[u]["coord"][1], G.nodes[u]["coord"][0]), tooltip=u,
                      icon=folium.Icon(color="green")).add_to(m)

    folium.Marker(location=(G.nodes[end]["coord"][1], G.nodes[end]["coord"][0]), tooltip=end,
                  icon=folium.Icon(color="red")).add_to(m)

    m.save("route_map.html")
    print("\nRoute map saved as route_map.html")

    if input("Open map in browser? (y/n): ").strip().lower() == "y":
        webbrowser.open("route_map.html")

if __name__ == "__main__":
    main()
