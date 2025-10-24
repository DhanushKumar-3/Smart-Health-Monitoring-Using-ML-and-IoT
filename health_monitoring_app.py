from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    # Create 'patients' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            mobile TEXT UNIQUE
        )
    ''')

    # Create 'prescriptions' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER,
            prescription TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create 'health_metrics' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pat_id INTEGER,
            bpm INTEGER,
            spo2 INTEGER,
            temperature REAL,
            humidity REAL,
            ppg REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Route for root
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Health Monitoring System"})

# Route for patient registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    age = data['age']
    gender = data['gender']
    mobile = data['mobile']

    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    # Check if patient exists by mobile number
    cursor.execute("SELECT pat_id FROM patients WHERE mobile = ?", (mobile,))
    existing = cursor.fetchone()

    if existing:
        pat_id = existing[0]
        message = "Existing patient found"
    else:
        cursor.execute(
            "INSERT INTO patients (name, age, gender, mobile) VALUES (?, ?, ?, ?)",
            (name, age, gender, mobile)
        )
        conn.commit()
        pat_id = cursor.lastrowid
        message = "New patient registered"

    conn.close()
    return jsonify({'message': message, 'pat_id': pat_id})

# Route for saving prescription
@app.route('/prescription', methods=['POST'])
def save_prescription():
    data = request.get_json()
    pat_id = data['pat_id']
    prescription = data['prescription']

    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    # Insert the prescription into the prescriptions table
    cursor.execute(
        "INSERT INTO prescriptions (pat_id, prescription) VALUES (?, ?)",
        (pat_id, prescription)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Prescription saved successfully'})

# Route for retrieving the latest prescription for a patient
@app.route('/prescription/<int:pat_id>', methods=['GET'])
def get_latest_prescription(pat_id):
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT prescription FROM prescriptions
        WHERE pat_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (pat_id,))

    row = cursor.fetchone()
    conn.close()

    return jsonify({'prescription': row[0] if row else 'No prescription available.'})

# Route for saving health metrics
@app.route('/health_metrics', methods=['POST'])
def save_health_metrics():
    data = request.get_json()
    pat_id = data['pat_id']
    bpm = data['bpm']
    spo2 = data['spo2']
    temperature = data['temperature']
    humidity = data['humidity']
    ppg = data['ppg']

    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    # Insert the health metrics into the health_metrics table
    cursor.execute(
        "INSERT INTO health_metrics (pat_id, bpm, spo2, temperature, humidity, ppg) VALUES (?, ?, ?, ?, ?, ?)",
        (pat_id, bpm, spo2, temperature, humidity, ppg)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Health metrics saved successfully'})

# Route for retrieving the latest health metrics for a patient
@app.route('/health_metrics/<int:pat_id>', methods=['GET'])
def get_latest_health_metrics(pat_id):
    conn = sqlite3.connect('patients.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT bpm, spo2, temperature, humidity, ppg FROM health_metrics
        WHERE pat_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (pat_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            'bpm': row[0],
            'spo2': row[1],
            'temperature': row[2],
            'humidity': row[3],
            'ppg': row[4]
        })
    else:
        return jsonify({'message': 'No health metrics available.'})

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
