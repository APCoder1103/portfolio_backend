from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import csv
import os
from datetime import datetime

app = Flask(__name__)

# ✅ Allow cross-origin requests to /api/* (including your uta.cloud site)
# You can restrict "origins" later if you want, but "*" is easiest for now.
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)


# ✅ Contact endpoint
@app.route("/api/contact", methods=["POST", "OPTIONS"])
@cross_origin(origins="*", methods=["POST", "OPTIONS"], headers=["Content-Type"])
def contact():
    # Handle CORS preflight request explicitly
    if request.method == "OPTIONS":
        # No body needed; CORS headers are added by flask-cors
        return "", 204

    # ---- Normal POST handling starts here ----
    try:
        data = request.get_json(force=True) or {}
    except Exception:
        return jsonify({"success": False, "error": "Invalid JSON body"}), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    # Basic validation to match what the frontend expects
    if not name or not email or not message:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    # ✅ Log messages into a CSV file
    file_path = "messages.csv"
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp_utc", "name", "email", "message"])
            writer.writerow([datetime.utcnow().isoformat(), name, email, message])
    except Exception as e:
        # If file writing fails, return a clear error for your toast
        return jsonify({"success": False, "error": f"Server error: {e}"}), 500

    # What your frontend expects on success
    return jsonify({"success": True}), 200


# Simple health check so you can see if the backend is up
@app.route("/")
def index():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
