import base64
import io
import os
import pickle

import cv2
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf

MODEL_PATH = os.environ.get("MODEL_PATH", "FinalTuberculosisModel.pkl")
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


def get_gradcam_heatmap(model_obj, img_array):
    try:
        if not hasattr(model_obj, "layers"):
            return None

        last_conv_layer = None
        for layer in reversed(model_obj.layers):
            if "conv" in layer.name.lower() or isinstance(
                layer, tf.keras.layers.Conv2D
            ):
                last_conv_layer = layer
                break

        if last_conv_layer is None:
            return None

        grad_model = tf.keras.models.Model(
            inputs=[model_obj.inputs],
            outputs=[last_conv_layer.output, model_obj.output],
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            if predictions.shape[-1] == 1:
                class_channel = predictions[0]
            else:
                pred_index = tf.argmax(predictions[0])
                class_channel = predictions[:, pred_index]

        grads = tape.gradient(class_channel, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()
    except Exception as e:
        print(f"Grad-CAM generation error: {e}")
        return None


def overlay_heatmap(original_img_np, heatmap, alpha=0.4):
    """Superimpose heatmap onto original image"""
    heatmap = cv2.resize(heatmap, (original_img_np.shape[1], original_img_np.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    original_img_bgr = cv2.cvtColor(
        (original_img_np * 255).astype(np.uint8), cv2.COLOR_RGB2BGR
    )
    superimposed_img = cv2.addWeighted(
        original_img_bgr, 1 - alpha, heatmap, alpha, 0
    )
    superimposed_img = cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)

    pil_img = Image.fromarray(superimposed_img)
    buffered = io.BytesIO()
    pil_img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


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

    img = Image.open(file.stream).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr_input = arr.reshape(1, 224, 224, 3)

    preds = model.predict(arr_input)
    preds_np = np.array(preds)

    if preds_np.ndim == 2:
        idx = int(np.argmax(preds_np[0]))
    else:
        idx = int(np.argmax(preds_np))

    gradcam_b64 = None
    heatmap = get_gradcam_heatmap(model, arr_input)
    if heatmap is not None:
        gradcam_b64 = overlay_heatmap(arr, heatmap)

    return jsonify(
        {"prediction": LABELS.get(idx, "Unknown"), "gradcam": gradcam_b64}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)