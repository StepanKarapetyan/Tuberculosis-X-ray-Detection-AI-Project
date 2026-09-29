const fileInput = document.getElementById('file-input');
const displayImage = document.getElementById('display-image');
const gradcamImage = document.getElementById('gradcam-image');
const gradcamBox = document.getElementById('gradcam-box');
const predictBtn = document.getElementById('predict-btn');
const resultDiv = document.getElementById('result');
const resetBtn = document.getElementById('reset-btn');

fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            displayImage.src = e.target.result;
            gradcamBox.style.display = "none";
            gradcamImage.src = "";
            resultDiv.innerText = "Image uploaded. Ready to predict.";
            resultDiv.style.color = "#34495e";
        }

        reader.readAsDataURL(file);
    }
});

resetBtn.addEventListener('click', () => {
    displayImage.src = "https://via.placeholder.com/300?text=Upload+X-Ray";
    gradcamImage.src = "";
    gradcamBox.style.display = "none";

    fileInput.value = "";

    resultDiv.innerText = "Waiting for image upload...";
    resultDiv.style.color = "#34495e";
    resultDiv.style.backgroundColor = "transparent";
});

predictBtn.addEventListener('click', async () => {
    if (fileInput.files.length === 0) {
        resultDiv.innerText = "Please select an image first!";
        resultDiv.style.color = "#e67e22";
        return;
    }

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    resultDiv.innerText = "AI is analyzing... Please wait.";
    resultDiv.style.color = "#3498db";

    try {
        const apiUrl =
            window.location.protocol === "file:"
                ? "http://127.0.0.1:8000/predict/"
                : "/predict/";

        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error("Connection failed");

        const data = await response.json();

        // Ցուցադրում ենք Grad-CAM heatmap-ը, եթե առկա է
        if (data.gradcam) {
            gradcamImage.src = "data:image/jpeg;base64," + data.gradcam;
            gradcamBox.style.display = "flex";
        } else {
            gradcamBox.style.display = "none";
        }

        if (data.prediction === "Tuberculosis" || data.prediction === "Positive") {
            resultDiv.innerHTML = "<strong style='color: #e74c3c;'>RESULT: TUBERCULOSIS DETECTED</strong>";
        } else if (data.prediction === "Normal" || data.prediction === "Negative") {
            resultDiv.innerHTML = "<strong style='color: #27ae60;'>RESULT: HEALTHY (NO INFECTION)</strong>";
        } else {
            resultDiv.innerText = "Result: " + data.prediction;
        }

    } catch (error) {
        console.error("Error:", error);
        resultDiv.innerText = "Error: Backend server is not responding.";
        resultDiv.style.color = "#c0392b";
    }
});