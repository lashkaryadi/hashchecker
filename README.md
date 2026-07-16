# Scam & URL Threat Detection Application

An advanced AI-powered web application designed to analyze text/email content for scam attempts and classify URLs to detect malicious threats. The app is built using Python, Flask, and the Google Gemini AI (using the `gemini-3.5-flash` model).

---

##  Features

1. **Scam/Fake Email Detection**:
   * Upload `.txt` or `.pdf` files (like suspicious emails, messages, or documents).
   * Extracts text and uses Gemini AI to analyze if the content is **Real/Legitimate** or a **Scam/Fake**.
   * Provides detailed reasoning for the classification.

2. **URL Threat Detection**:
   * Analyzes input URLs and classifies them into security categories:
     * **Benign**: Safe, trusted, and non-malicious websites.
     * **Phishing**: Fraudulent websites designed to steal credentials.
     * **Malware**: URLs that distribute viruses or ransomware.
     * **Defacement**: Hacked or defaced websites displaying unauthorized content.

---

##  Tech Stack

* **Backend**: Flask (Python)
* **Frontend**: HTML5, Vanilla CSS, FontAwesome Icons (Responsive UI)
* **AI Model**: Google Gemini AI (`gemini-3.5-flash`)
* **Libraries**: `google-generativeai`, `PyPDF2`, `python-dotenv`

---

##  Setup & Installation

### Prerequisites
* Python 3.10+ installed on your system.
* A Gemini API key. Get one from the [Google AI Studio](https://aistudio.google.com/).

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Detect-Scam-Emails-Malicious-URLs-with-FastAPI-Gemini-AI-Build-a-Scam-Detection-App-.git
cd Detect-Scam-Emails-Malicious-URLs-with-FastAPI-Gemini-AI-Build-a-Scam-Detection-App-
```

### 2. Configure Environment Variables
Create a file named `.env` in the root directory and add your Google API key:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key
```

### 3. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python main.py
```

Open your browser and navigate to:
**[http://127.0.0.1:8080](http://127.0.0.1:8080)**

*(Note: The default port is configured to `8080` to avoid conflicts with macOS built-in services on port `5000`).*

---

##  Deployment

This project is ready to deploy to production hosting platforms like **Render** or **Railway**.

### Render Deployment Steps:
1. Push your code to a GitHub repository (ensuring `.env` and `.venv/` are excluded via `.gitignore`).
2. Create a new **Web Service** on Render and connect your repository.
3. Configure the settings:
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn main:app`
4. Add the following Environment Variable in the **Environment** tab:
   * Key: `GOOGLE_API_KEY`
   * Value: *Your Gemini API Key*
5. Click **Deploy**.