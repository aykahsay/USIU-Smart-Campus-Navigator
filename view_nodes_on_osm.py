import geopandas as gpd
import folium
import ast

# Load your cleaned GeoJSON
gdf = gpd.read_file("data/combined_cleaned_routes.geojson")

# Initialize folium map centered on USIU
m = folium.Map(location=[-1.217, 36.878], zoom_start=17)

for idx, row in gdf.iterrows():
    try:
        # Parse coords safely
        start_coord = row["start_coord"]
        end_coord = row["end_coord"]

        if isinstance(start_coord, str):
            start_coord = ast.literal_eval(start_coord)
        if isinstance(end_coord, str):
            end_coord = ast.literal_eval(end_coord)

        # ➕ Draw edge (LineString)
        if row.geometry and row.geometry.geom_type == "LineString":
            coords = [(lat, lon) for lon, lat in row.geometry.coords]
            folium.PolyLine(coords, color="blue", weight=3, opacity=0.7).add_to(m)

        # 🟦 Start marker
        folium.Marker(
            location=[start_coord[1], start_coord[0]],
            popup=f"Start: {row['start_name']}",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

        # 🟥 End marker
        folium.Marker(
            location=[end_coord[1], end_coord[0]],
            popup=f"End: {row['end_name']}",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m)

    except Exception as e:
        print(f"⚠️ Skipped row {idx}: {e}")

# Save map
m.save("static/node_map_osm.html")
print("✅ Node + Edge map saved to: static/node_map_osm.html")
