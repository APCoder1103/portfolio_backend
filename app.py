from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Allow your uta.cloud domain (and localhost for testing) to call the API
CORS(app, origins=[
    "https://prh2350.uta.cloud",
    "http://localhost",
    "http://127.0.0.1"
])


PROJECTS = [
    {
        "title": "Cyclistic Bike-Sharing Case Study",
        "date": "Aug 2024 – Present",
        "description": (
            "Analyzed hundreds of thousands of ride records using Google BigQuery "
            "and Google Cloud. Cleaned, transformed, and modeled data to explore "
            "usage patterns and created visualizations in Excel and Tableau."
        ),
        "tools": "Google BigQuery, Google Cloud, Excel, Tableau",
    },
    {
        "title": "Employee Performance Database (SQL Server)",
        "date": "Nov 2024",
        "description": (
            "Designed and implemented a relational database for tracking employee "
            "performance to practice SQL Server and demonstrate proactive learning."
        ),
        "tools": "SQL Server",
    },
    {
        "title": "Bellabeat Case Study",
        "date": "Aug 2024 – Present",
        "description": (
            "Performed a data analytics case study in Python, exploring user activity "
            "data and generating insights for a wellness-focused product."
        ),
        "tools": "Python, pandas",
    }
]


@app.get("/api/projects")
def get_projects():
    """Return project data as JSON."""
    return jsonify(PROJECTS)


@app.post("/api/contact")
def submit_contact():
    """Receive contact form data and append to a CSV file."""
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "error": "All fields are required."}), 400

    row = [datetime.utcnow().isoformat(), name, email, message]

    file_exists = os.path.isfile("contact_messages.csv")
    with open("contact_messages.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp_utc", "name", "email", "message"])
        writer.writerow(row)

    return jsonify({"ok": True})


if __name__ == "__main__":
    # Local development
    app.run(debug=True)
