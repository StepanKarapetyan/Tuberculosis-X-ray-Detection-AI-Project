## Tuberculosis X-ray Detection AI Project 🫁🤖

An Artificial Intelligence and Deep Learning application designed to detect Tuberculosis (TB) from Chest X-ray images using Computer Vision and a Web Interface.

## 📌 Overview

Tuberculosis (TB) is a serious infectious disease affecting the lungs. Early and accurate detection is critical for effective treatment. This project utilizes a trained Machine Learning / Deep Learning model saved as a `.pkl` file, paired with a Python web server (`server.py`) and a frontend UI (`index.html`, `style.css`, `script.js`) to allow users to upload chest X-ray images and get predictions in real time.

## 🗂️ Project Structure

```
Tuberculosis-X-ray-Detection-AI-Project/
│
├── venv/                           # Virtual Environment (ignored by Git)
├── FinalTuberculosisModel.pkl      # Trained model file
├── Tuberculosis.ipynb              # Notebook for model training & analysis
├── server.py                       # Backend server API
├── index.html                      # Frontend HTML interface
├── style.css                       # Frontend styling
├── script.js                       # Frontend interaction & API calls
├── requirements.txt                # Dependencies
└── README.md                       # Project documentation

```

## 🛠️ Tech Stack & Requirements

* **Python 3.11․4**

* **Frontend:** HTML5, CSS3, JavaScript

* **Backend:** Python (Flask / FastAPI)

* **ML & Processing:** OpenCV, NumPy, Pandas, Matplotlib, Scikit-learn / TensorFlow / PyTorch, Joblib / Pickle

All Python dependencies are listed in `requirements.txt`.

## 🚀 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/StepanKarapetyan/Tuberculosis-X-ray-Detection-AI-Project.git
cd Tuberculosis-X-ray-Detection-AI-Project

```

### 2. Set Up Virtual Environment

It is recommended to use a virtual environment:

```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```
pip install -r requirements.txt

```

### 4. Run the Application Server

Start the backend server:

```
python server.py

```

Open your browser and navigate to the address shown in your terminal (usually `http://127.0.0.1:5000` or `http://localhost:8000`) to access the interface.

## 📓 Model Training

To see how the model was trained, preprocessed, or evaluated, open and run the Jupyter Notebook:

```
jupyter notebook Tuberculosis.ipynb

```

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

## 📽️ Demo / Preview

(https://github.com/user-attachments/assets/5a197b66-9aab-4263-9e60-a1f1b3284280)
