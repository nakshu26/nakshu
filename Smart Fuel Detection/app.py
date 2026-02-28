from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect("fuel.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuel REAL,
            mileage REAL,
            distance REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    fuel = float(request.form["fuel"])
    mileage = float(request.form["mileage"])

    distance = fuel * mileage

    alert = ""
    if distance < 50:
        alert = "⚠ Low Fuel! Please refill soon."

    # Save to database
    conn = sqlite3.connect("fuel.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO fuel_data (fuel, mileage, distance, date) VALUES (?, ?, ?, ?)",
        (fuel, mileage, distance, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

    return render_template("result.html", distance=distance, alert=alert)

@app.route("/history")
def history():
    conn = sqlite3.connect("fuel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fuel_data")
    data = cursor.fetchall()
    conn.close()
    return render_template("history.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)