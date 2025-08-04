# USIU-Smart-Campus-Navigator
An Intelligent Route Mapping System for USIU-Africa Visitors and Community

# 📍 USIU Smart Campus Routing Application

## 🗺️ Overview

This application provides intelligent navigation within the **United States International University (USIU)** campus. It helps **visitors, staff, students, and persons with disabilities** find optimal routes between buildings, parking lots, fire assembly points, gates, outdoor game zones, and other venues.

The system considers **real-time conditions** such as time of day, human or vehicle traffic, wheelchair accessibility, and the user's **mode of transport (walking or driving)**. It supports both **single-destination** and **multi-destination** routing, and visualizes recommended paths on a map.

---

## ✅ Key Features

- 🔎 **Route Recommendation**: Provides best paths based on:
  - Distance (shortest)
  - Estimated traffic (human/vehicle)
  - Time/day (e.g., class transition hours)
  - Wheelchair accessibility
  - Mode of transport (walking vs. driving)

- 🧭 **Multi-Destination Routing**: Calculates the best sequence and path to visit multiple venues.

- 🧠 **Heuristic Routing**: Uses **Euclidean distance** for quick estimations.

- 🚧 **Admin Control**: Admin can **temporarily disable paths** under construction or unusable.

- 🗺️ **Interactive Map Visualization**: Displays routes, venues, and user paths using **GeoJSON and GeoPandas**.

---

## 🛠️ Tech Stack

- **Python** (3.11+)
- **GeoPandas** – for geospatial data handling
- **NetworkX** – for graph-based path computation
- **Matplotlib / Folium** – for route visualization
- **Shapely** – for geometric operations

---

## 📂 Folder Structure

```
usiu-routing-app/
│
├── data/
│   └── combined_usiu_paths.geojson      # Path network with geometry and metadata
│
├── main.py                              # Entry point for route calculation
├── utils.py                             # Helper functions for routing and visualization
├── admin.py                             # Admin utilities for enabling/disabling paths
├── config.py                            # Time/day conditions, accessibility rules
└── README.md                            # This file
```

---

## 🚀 Getting Started

### 1. 📥 Installation

Ensure Python is installed, then:

```bash
pip install geopandas networkx matplotlib shapely
```

### 2. 📂 Prepare Your Data

Ensure `combined_usiu_paths.geojson` is placed inside the `data/` folder.

Each feature must have:

- `geometry`: LineString for paths
- `name`: Path or location name
- `length_m`: Length in meters
- `accessible`: Boolean for wheelchair access
- `vehicle`: Boolean for vehicle access

### 3. 🧪 Run Example

```bash
python main.py
```

Follow the prompts to select:

- Start & destination
- Time & day
- Transport mode
- Accessibility preference

---

## 🧮 How Routing Works

1. **Graph Construction**: Converts LineString paths into a weighted graph using `NetworkX`.
2. **Weight Assignment**: Weights depend on:
   - Path length
   - Traffic estimates based on time/day
   - Access type (e.g., walking vs. driving)
3. **Shortest Path Algorithm**: Uses `Dijkstra` or `A*` with Euclidean heuristic.
4. **Visualization**: Highlights recommended route(s) on the map.

---

## 🛑 Admin Features

- Disable or re-enable any path using `admin.py`.
- Temporarily removed paths are ignored during routing.

---

## 📊 Future Improvements

- Real-time data integration (e.g., crowd sensors or gate logs)
- Mobile/web interface with interactive UI
- Voice-guided navigation for visually impaired users
