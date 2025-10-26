from flask import Flask, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.path.join("data", "attendance.json")

# Ensure data folder exists
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_records():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_records(records):
    with open(DATA_FILE, "w") as f:
        json.dump(records, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/save", methods=["POST"])
def save_attendance():
    data = request.get_json()
    if not data or "date" not in data or "records" not in data:
        return jsonify({"error": "Invalid data"}), 400

    records = load_records()
    # Replace if date exists
    existing = next((r for r in records if r["date"] == data["date"]), None)
    if existing:
        records = [r for r in records if r["date"] != data["date"]]
    data["savedAt"] = datetime.now().isoformat()
    records.append(data)
    save_records(records)
    return jsonify({"message": "Attendance saved"}), 200

@app.route("/api/records", methods=["GET"])
def get_records():
    return jsonify(load_records())

@app.route("/api/delete/<date>", methods=["DELETE"])
def delete_record(date):
    records = load_records()
    records = [r for r in records if r["date"] != date]
    save_records(records)
    return jsonify({"message": f"Deleted records for {date}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
