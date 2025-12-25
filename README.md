# ✈️ FlightVision – AI-Powered Flight ETA Prediction System

FlightVision is a real-time aviation analytics web application that tracks live aircraft positions and predicts estimated time of arrival (ETA) using geospatial calculations and AI-based estimation. The system leverages live aviation data APIs and visualizes insights through an interactive Streamlit dashboard.

---

## 🚀 Features

* 🔴 **Live Flight Tracking** – Fetches real-time aircraft position data
* 🧠 **AI-Based ETA Prediction** – Estimates landing time using distance & speed
* 🌍 **Geospatial Calculations** – Uses Haversine formula for accurate distance
* 📊 **Interactive Dashboard** – Tables, charts, and maps powered by Streamlit
* 🗺️ **Live Map Visualization** – Displays real-time aircraft locations

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit** – Web interface
* **Pandas** – Data processing
* **AviationStack API** – Live flight & airport data
* **Geospatial Math (Haversine Formula)**
* **REST APIs**

---

## 📂 Project Structure

```
FlightVision/
│
├── app.py                 # Main Streamlit app
├── api_client.py          # API calls for flights & airports
├── prediction.py          # ETA prediction logic
├── utils.py               # Haversine distance calculation
├── config.py              # API key configuration
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## 🔑 API Configuration

1. Create a free account at **AviationStack**
2. Get your API key
3. Create a `config.py` file:

```python
API_KEY = "YOUR_API_KEY_HERE"
```

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the application

```bash
streamlit run app.py
```

### 3️⃣ Open in browser

```
http://localhost:8501
```

---

## 📈 How ETA is Calculated

1. Fetch live aircraft latitude & longitude
2. Fetch destination airport coordinates
3. Calculate distance using **Haversine formula**
4. Estimate arrival time using aircraft speed
5. Convert hours → minutes for ETA

---

## ⚠️ Limitations

* ETA accuracy depends on live speed availability
* Some flights may not expose arrival airport data
* Weather, air traffic & routing are not yet modeled

---

## 🌱 Future Improvements

* 🤖 Machine Learning regression for smarter ETA
* 🛬 Flight route path visualization
* ☁️ Weather impact modeling
* 📡 Caching & API optimization
* 🧪 Historical flight data analysis

---

## 🎯 Use Cases

* Aviation analytics demos
* AI/ML portfolio projects
* Real-time data visualization
* Geospatial AI applications

---

## 👨‍💻 Author

**Sayed Faisal Shah**
AI & Flutter Developer | ML Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork or extend it!
