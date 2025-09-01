# 🧭 USIU Smart Campus Navigator

**Project Overview:**  
The **USIU Smart Campus Navigator** is a web-based interactive application designed to help students, staff, and visitors navigate the **USIU-Africa campus** efficiently. It provides optimal routes between campus locations, considering accessibility, route type, traffic conditions, and travel time.  

This project leverages **Python**, **Flask**, **NetworkX**, **GeoPandas**, **Folium**, and **Matplotlib** for routing, visualization, and GIS integration.

---

## 👩‍🏫 Course Mentor
This project was developed under the guidance of **[Mutanu, Leah, PhD](https://www.usiu.ac.ke/1204/mutanu-leah-phd-/?schl=sst)**, who served as the course professor and mentor for this project.

---

## 🗂️ Folder Structure

```

USIU-Campus-Navigator/
│
├─ app.py                 # Main Flask application
├─ requirements.txt       # Python dependencies
├─ README.md              # Project documentation
│
├─ templates/             # HTML templates
│   ├─ index.html         # User interface for route planning
│   ├─ admin.html         # Admin interface for disabling routes
│   └─ login.html         # Admin login page
│
├─ static/                # Static files (maps, CSS, JS)
│   └─ route\_map.html     # Generated Folium map
│
├─ data/                  # Spatial and routing data
│   ├─ combined\_cleaned\_routes.geojson      # Cleaned campus route data
│   └─ disabled\_routes.json                 # Disabled edges configuration
│
└─ notebooks/             # Optional Jupyter notebooks for analysis & visualization
└─ route\_visualization.ipynb

````

---

## 🛠️ Features

- **User Functionality**
  - Select **start** and **end** locations.  
  - Add up to **3 intermediate stops**.  
  - Choose **route type**: pedestrian, car, or any.  
  - Filter for **wheelchair accessible** paths.  
  - View the suggested route on a dynamic **Folium map**.  
  - Travel time annotated for each route segment, accounting for **traffic**.
<img width="1546" height="881" alt="image" src="https://github.com/user-attachments/assets/58a2c6eb-9f01-4260-becf-8890b1d5243d" />

- **Admin Functionality**
  - Login with secure password.  
  - Enable or disable specific campus routes.  
  - Changes persist in `disabled_routes.json`.

- **Routing Algorithms**
  - **A\*** search algorithm for pathfinding.  
  - **Euclidean distance heuristic** to estimate cost between nodes.  
  - Weighted edges consider **distance**, **average speed**, and **traffic factor**.
<img width="1359" height="668" alt="image" src="https://github.com/user-attachments/assets/52b47f1b-ed7a-4918-b1d0-1ba4c501eb0d" />

- **Traffic & Accessibility**
  - Pedestrian routes assume ~1.5 m/s, car routes ~10 m/s.  
  - Traffic levels: `low`, `medium`, `high`, affecting travel time.  
  - Wheelchair accessibility enforced if selected by user.

---

## 🗺️ Visualization

- Interactive campus map using **Folium**, with:
  - **Green**: pedestrian routes  
  - **Blue**: car routes  
  - **Red**: suggested path  
  - Travel time annotated along each segment  

- Optional **NetworkX visualization** to display the network, highlight key nodes, and show traffic conditions.

<img width="1589" height="1390" alt="image" src="https://github.com/user-attachments/assets/1375113a-3b03-41fe-a843-528d5208e073" />

---

## 📁 Data Sources

This project uses spatial data from **OpenStreetMap** and custom digitization of the **USIU-Africa campus layout**.

- **OpenStreetMap contributors.** (n.d.). [OpenStreetMap](https://www.openstreetmap.org)  
- **Custom digitized data** prepared manually in QGIS by the project team.  

**Details:**
- All paths and routing data were downloaded and cleaned from OpenStreetMap (OSM).  
- File format: **GeoJSON**  
- Each route represents a **LineString** connecting a named origin to a destination.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+  
- Packages listed in `requirements.txt` (install via `pip install -r requirements.txt`)  

### Running the Application
```bash
# Set environment variables (optional)
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"

# Run the Flask app
python -m flask run
````

* **User interface:** [http://127.0.0.1:5000/](https://38e81215d827.ngrok-free.app
)
* **Admin panel:** [http://127.0.0.1:5000/admin](https://38e81215d827.ngrok-free.app/login)

**Default admin password:** `admin123` (change in `app.py` for security)

---

## ⚙️ Technical Details

* **Graph Construction**

  * Nodes: campus landmarks, gates, parking lots, libraries, classrooms
  * Edges: routes between nodes, with distance, type, average speed, and traffic factor

* **Routing Algorithm**

  * A\* pathfinding implemented using **NetworkX**
  * Euclidean distance as heuristic for efficient route calculation

* **Travel Time Calculation**

```python
time_sec = distance / avg_speed * traffic_factor
time_min = round(time_sec / 60, 1)
```

* **Visualization**

  * `Folium` for interactive maps
  * `Matplotlib` for static network plots with traffic overlay

---

## 📝 References

* [OpenStreetMap](https://www.openstreetmap.org)
* Mutanu, Leah, PhD – [USIU Faculty Page](https://www.usiu.ac.ke/1204/mutanu-leah-phd-/?schl=sst)

---

## 💡 Future Improvements

* Integrate **real-time traffic** updates.
* Add **public transport routes** on campus.
* Mobile-friendly interface for smartphones.
* Route optimization for multiple users or events.

```
