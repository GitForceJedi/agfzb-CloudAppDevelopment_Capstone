import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Django API URL (Update this with your actual Render Django URL)
DJANGO_API_URL = "https://your-django-app.onrender.com/djangoapp/"


@app.route("/reviews/get", methods=["GET"])
def get_reviews():
    dealership_id = request.args.get("dealership")

    try:
        response = requests.get(f"{DJANGO_API_URL}reviews/", params={"dealership": dealership_id})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch reviews from Django: {str(e)}"}), 500


@app.route("/reviews/post", methods=["POST"])
def post_review():
    try:
        review_data = request.json  # Get JSON payload
        response = requests.post(f"{DJANGO_API_URL}reviews/add/", json=review_data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to post review to Django: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Use Render's PORT, default to 5001 locally
    app.run(host="0.0.0.0", port=port)
