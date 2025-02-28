import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Django API URL (Update with your actual Render Django URL)
DJANGO_API_URL = "https://your-django-app.onrender.com/djangoapp/"

@app.route("/dealerships/get", methods=["GET"])
def get_dealerships():
    state = request.args.get("state")
    id = request.args.get("id")

    try:
        response = requests.get(f"{DJANGO_API_URL}dealerships/", params={"state": state, "id": id})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data from Django: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT, default to 5000 locally
    app.run(host="0.0.0.0", port=port)
