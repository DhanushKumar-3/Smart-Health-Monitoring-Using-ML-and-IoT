# Smart-Health-Monitoring-Using-ML-and-IoT
# Smart Health Monitoring System

A simple health monitoring prototype that:

* Trains a K-Nearest Neighbors (KNN) model on vital signs (BPM, SpO2, Temperature, PPG).
* Streams readings from an ESP8266, predicts health status, and uploads to ThingSpeak.
* Provides a Flask API for patient registration, prescriptions, and health data storage via SQLite.

## Repository Structure

* **KNN.py** – Trains a 1-NN model using `data.csv` and saves it as `model.sav`.
* **data.csv** – Dataset with columns: BPM, SpO2, Temperature, PPG, Label.
* **final.py** – Fetches sensor data from ESP8266, predicts label, uploads to ThingSpeak.
* **health_monitoring_app.py** – Flask app managing patients, prescriptions, and metrics.
* **ESP_Wahaj.h** – ESP8266 Wi-Fi and HTTP helper for sensor data serving.

## Features

* KNN model training and evaluation.
* Local prediction and ThingSpeak publishing.
* Flask REST API for CRUD operations.
* Simple ESP8266 data streaming support.

## Quick Start

1. **Install dependencies**

   ```
   pip install flask flask-cors numpy pandas scikit-learn seaborn matplotlib requests
   ```
2. **Train the model**

   ```
   python KNN.py
   ```
3. **Run Flask API**

   ```
   python health_monitoring_app.py
   ```
4. **Run prediction script**

   ```
   python final.py
   ```

## Flask API Endpoints

* `GET /` – Welcome message
* `POST /register` – Register or retrieve patient
* `POST /prescription` – Save prescription
* `GET /prescription/<pat_id>` – Get latest prescription
* `POST /health_metrics` – Save metrics
* `GET /health_metrics/<pat_id>` – Get latest metrics

## SQLite Tables

* **patients**(pat_id, name, age, gender, mobile)
* **prescriptions**(id, pat_id, prescription, timestamp)
* **health_metrics**(id, pat_id, bpm, spo2, temperature, humidity, ppg, timestamp)

## Known Issues

* No authentication (add API keys/JWT).
* Minimal validation.
* Hardcoded IP in `final.py`.
* ESP code needs better request handling.

## Run End-to-End

1. Train model with `KNN.py`.
2. Start Flask API.
3. Run ESP8266 sketch to serve sensor values.
4. Execute `final.py` to get predictions and upload to ThingSpeak.

## License

## Acknowledgements

scikit-learn, Flask, SQLite, ThingSpeak.
