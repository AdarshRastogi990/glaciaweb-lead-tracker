from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re # Yeh Regular Expression library hai, email check karne ke kaam aati hai

app = Flask(__name__)
# CORS security guard ko batata hai ki kisi aur port (jaise React ka port) se aane wali request ko allow karo
CORS(app) 

from flask import redirect

@app.route("/")
def home():
    return redirect("/api/leads")

# Database connect karne ka function
def get_db_connection():
    # hum database file ka naam 'leads.db' rakh rahe hain
    conn = sqlite3.connect('leads.db')
    # isse data humein dictionary (key-value) format mein milega, jo API ke liye asaan hota hai
    conn.row_factory = sqlite3.Row 
    return conn

# App start hone par table banane ka function
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Execute command ek SQL query chalati hai. Ye tabhi table banayegi jab wo pehle se nahi hogi.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            service_required TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit() # Data save karne ke liye commit karna zaroori hai
    conn.close() # Kaam hone ke baad connection close karna safe practice hai

# Ye function jab file run hogi tabhi database set kar dega
init_db()

# --- ROUTES (API ENDPOINTS) ---

# 1. GET Route: Saare leads fetch karne ke liye
@app.route('/api/leads', methods=['GET'])
def get_leads():
    try:
        conn = get_db_connection()
        leads = conn.execute('SELECT * FROM leads').fetchall()
        conn.close()
        
        # Data ko JSON format mein badal kar frontend ko bhej rahe hain
        return jsonify([dict(ix) for ix in leads]), 200
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# 2. POST Route: Naya lead add karne ke liye
@app.route('/api/leads', methods=['POST'])
def add_lead():
    # Frontend se aane wale data ko receive karna
    data = request.json 
    
    # Validation Rules (Interface Safety)
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    service_required = data.get('service_required', '').strip()
    status = data.get('status', 'Pending').strip()

    # Agar koi input khali hai, toh error throw karo
    if not name or not email or not service_required:
        print("Validation Failed: Missing required fields.")
        return jsonify({"error": "Name, Email, and Service are required!"}), 400

    # Email format check karne ka basic rule
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Validation Failed: Invalid Email Format.")
        return jsonify({"error": "Invalid Email Format!"}), 400

    # Database mein data daalne ka try-except block (Correctness & Resilience)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leads (name, email, service_required, status) VALUES (?, ?, ?, ?)',
            (name, email, service_required, status)
        )
        conn.commit()
        conn.close()
        
        # Observability: Terminal mein print karna
        print(f"Success: New lead added -> {name} ({email})")
        return jsonify({"message": "Lead added successfully!"}), 201

    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"error": "Failed to add lead to database."}), 500

# App ko run karne ki command
if __name__ == '__main__':
    # debug=True ka matlab hai code save karte hi server khud refresh ho jayega
    app.run(debug=True, port=5000)