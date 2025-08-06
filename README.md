Here’s a complete and professional `README.md` file for your GitHub project: **USIU Smart Campus Navigator**. You can copy and paste it into your repo root.

---

```markdown
# 🧭 USIU Smart Campus Navigator

An intelligent campus map system for **United States International University - Africa (USIU-Africa)**. This application helps students, staff, and visitors find optimal routes between various buildings, gates, parking lots, sports fields, and more — whether walking, driving, or using a wheelchair.

---

## 📌 Features

- 🗺️ Interactive map powered by **Folium** + **OpenStreetMap**
- 🧠 Smart route recommendations:
  - Based on **mode of transport**: Pedestrian, Car, Wheelchair
  - Considers **time/day context** (e.g. after class, weekends)
  - Uses **shortest path** and **A* heuristic (Euclidean distance)**
- ♿ Wheelchair accessibility
- ➕ Multi-stop routing (Traveling Salesman-style)
- 🛠️ Admin functionality to **disable/enable paths** temporarily
- 📍 Visual highlights of:
  - Start location
  - Destination
  - Suggested route

---

## 📂 Project Structure

```

USIU-Map-Navigator/
├── app.py                       # Flask application (main backend)
├── view\_nodes\_on\_osm.py        # Visualize nodes + edges on map
├── data/
│   └── combined\_cleaned\_routes.geojson   # Merged cleaned routing data
├── static/
│   └── node\_map\_osm.html       # Auto-generated Folium map
├── templates/
│   ├── index.html              # Homepage form
│   └── route\_map.html          # Map with selected route
├── requirements.txt
└── README.md

````

---

## 🚀 Setup & Run Locally

### 🛠️ Requirements

- Python 3.10+
- Flask
- GeoPandas
- NetworkX
- Folium
- Pyogrio
- Shapely

### 🔽 Install dependencies

```bash
pip install -r requirements.txt
````

### ▶️ Run the app

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Usage Instructions

1. Select:

   * **Start Location**
   * **End Location**
   * **Mode of Transport** (Pedestrian / Car / Wheelchair)
2. Click **Submit**
3. View the **optimal route on the map**

---

## 🗂️ Data Sources

* All paths and routing data were downloaded and cleaned from **OpenStreetMap (OSM)**.
* File format: `GeoJSON`
* Each route represents a `LineString` from a named origin to destination.

---

## 🧹 Node Cleaning and Standardization

Common typos and duplicate names were cleaned with a standardized mapping, e.g.:

* `Adminstartion Block` → `Administration Block`
* `Frieda Brown  Student Centere Parking Lot` → `Frieda Brown Student Center Parking Lot`
* `Pual's Caffe` → `Paul's Caffe`

---

## 📈 Future Enhancements

* 🧭 Indoor navigation within buildings
* 📅 Dynamic congestion levels based on timetable
* 🧠 ML-powered recommendations
* 📱 Android mobile version

---

## 🤝 Contributions

Contributions are welcome. Please open an issue first to discuss changes or improvements.

---

## © License

This project is developed for academic and educational use under the MIT License.

```
