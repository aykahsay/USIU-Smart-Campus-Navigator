# USIU Smart Campus Navigator

A Python-based route mapping tool to help users find the shortest paths between locations on the USIU campus using car or pedestrian routes.

---

## Features

- Supports two modes: **Car** and **Pedestrian** routing  
- Loads combined GeoJSON route data for each mode  
- Builds an undirected graph of campus paths using NetworkX  
- Calculates shortest path using Euclidean distance as edge weight  
- Interactive CLI to select mode, start, and end locations  
- Generates an interactive HTML map with the calculated route using Folium  
- Optionally opens the generated route map in a web browser  

---

## Requirements

- Python 3.10 or higher  
- Python libraries:
  - geopandas  
  - networkx  
  - folium  
  - shapely  

Install dependencies with:

```bash
pip install geopandas networkx folium shapely

Setup & Usage

    Place the following files in your project folder (e.g., USIU_Smart_Campus_Navigator/):

        app.py

        combined_car_routes_named.geojson

        combined_pedestrian_routes_named.geojson

    Run the app:

python app.py

    Follow prompts in the terminal:

        Select routing mode (car or pedestrian)

        View available locations for the selected mode

        Enter exact start location name

        Enter exact end location name

        Choose whether to open the route map in your browser

Data Format

The GeoJSON files should contain features with:

    start_name: Name of the starting point

    end_name: Name of the ending point

    route_name: (optional) Route identifier

    geometry: A LineString representing the path

How It Works

    Graph Building: The app reads the GeoJSON routes and creates an undirected graph where nodes are locations and edges are routes weighted by straight-line (Euclidean) distance.

    Routing: Uses NetworkX’s shortest path algorithm to find the minimal-distance route between selected locations.

    Visualization: The route is drawn on a Folium map saved as route_map.html. Markers show start and end points, and the path is highlighted.

Current Limitations

    Only supports shortest path by Euclidean distance (no real traffic or time considerations yet).

    Routing is bidirectional on all paths (no one-way streets).

    Interaction is via command-line interface (no GUI or mobile app yet).

    No multi-destination or accessibility filtering implemented yet.

Future Improvements (Planned)

    Support for multi-stop routing optimization

    Real-time data integration for traffic or accessibility

    Web or mobile app interface with interactive UI

    Admin features to disable or update routes dynamically

Folder Structure

UUSIU_Smart_Campus_Navigator/
│
├── data/
│   ├── combined_car_routes_named.geojson
│   ├── combined_pedestrian_routes_named.geojson
│   └── (any other raw or processed data files)
│
├── notebooks/
│   └── exploratory_analysis.ipynb       # Jupyter notebooks for analysis or prototyping
│
├── src/
│   ├── app.py                          # Main application script
│   └── utils.py                       # helper functions, e.g., graph building, routing
│
├── tests/
│   └── test_routing.py                # tests for your routing functions
│
├── .gitignore                        # To exclude files like __pycache__, .env, large data files
├── README.md                         # Project README file (you just got it!)
├── requirements.txt                  # List of Python dependencies for easy install
└── LICENSE                          # License file (e.g., MIT License)


License

MIT License © Amabchow and Samuel
