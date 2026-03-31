import os
import pickle

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

import numpy as np
from PIL import Image


MODEL_PATH = os.environ.get("MODEL_PATH", "../model (1).pkl")
LABELS = {0: "Normal", 1: "Tuberculosis"}


app = Flask(__name__, static_folder=".")
CORS(app)


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}. Set MODEL_PATH env var if needed."
        )
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


model = load_model()


@app.route("/")
def index():
    return send_from_directory("", "index.html")

@app.route("/style.css")
def style_css():
    return send_from_directory("", "style.css")


@app.route("/script.js")
def script_js():
    return send_from_directory("", "script.js")


@app.route("/predict/", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "Missing `image` file field"}), 400

    file = request.files["image"]
    if not file or not file.filename:
        return jsonify({"error": "Empty image file"}), 400

    img = Image.open(file.stream).convert("L")
    img = img.resize((150, 150))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = arr.reshape(1, 150, 150, 1)

    preds = model.predict(arr)
    preds = np.array(preds)

    if preds.ndim == 2:
        idx = int(np.argmax(preds[0]))
    else:
        idx = int(np.argmax(preds))

    return jsonify({"prediction": LABELS.get(idx, "Unknown")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

