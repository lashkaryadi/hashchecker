from flask import Flask, render_template, request
import os
import time
from google import genai
from google.genai import errors as genai_errors
import PyPDF2
from dotenv import load_dotenv
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Set up the Google API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Please configure it in your .env file or environment variables.")

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# functions
def predict_fake_or_real_email_content(text):
    prompt = f"""
    You are an expert in identifying scam messages in text, email etc. Analyze the given text and classify it as:

    - **Real/Legitimate** (Authentic, safe message)
    - **Scam/Fake** (Phishing, fraud, or suspicious message)

    **for the following Text:**
    {text}

    **Return a clear message indicating whether this content is real or a scam. 
    If it is a scam, mention why it seems fraudulent. If it is real, state that it is legitimate.**

    **Only return the classification message and nothing else.**
    Note: Don't return empty or null, you only need to return message for the input text
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )
            return response.text.strip() if response else "Classification failed."
        except genai_errors.ServerError as e:
            if e.status_code == 503 and attempt < 2:
                time.sleep(2 ** attempt)  # 1s, then 2s back-off
                continue
            return (
                "⚠️ The AI service is currently experiencing high demand. "
                "Please try again in a few seconds."
            )
        except genai_errors.ClientError as e:
            return f"⚠️ Request error: {e.message}. Please check your input and try again."
        except Exception:
            return "⚠️ An unexpected error occurred while analysing the content. Please try again."
    return "⚠️ The AI service did not respond after multiple retries. Please try again later."


KNOWN_CLASSES = ["benign", "phishing", "malware", "defacement"]


def normalize_url_class(raw: str) -> str:
    """Extract the first known class word from Gemini's raw response."""
    text = raw.lower().strip()
    for cls in KNOWN_CLASSES:
        if cls in text:
            return cls
    return "unknown"


def url_detection(url):
    prompt = f"""
    You are an advanced AI model specializing in URL security classification.
    Analyze the given URL and classify it as EXACTLY ONE of these four categories:

    - benign     : Safe, trusted websites (google.com, wikipedia.org, amazon.com)
    - phishing   : Sites designed to steal credentials — misspelled domains,
                   fake login pages, misleading subdomains (e.g. paypa1.com)
    - malware    : URLs that distribute viruses, ransomware, or trigger automatic
                   downloads of malicious software
    - defacement : Hacked/altered websites displaying unauthorized content

    Examples:
    https://www.microsoft.com/          -> benign
    http://secure-login.paypa1.com/     -> phishing
    http://free-download-software.xyz/  -> malware
    http://hacked-website.com/          -> defacement

    URL to classify: {url}

    IMPORTANT: Reply with ONLY the single lowercase class name and nothing else.
    Valid replies: benign | phishing | malware | defacement
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )
            raw = response.text.strip() if response else ""
            return normalize_url_class(raw)
        except genai_errors.ServerError as e:
            if e.status_code == 503 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            return None  # signals a server error
        except genai_errors.ClientError:
            return None
        except Exception:
            return None
    return None


# Routes

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/scam/', methods=['POST'])
def detect_scam():
    if 'file' not in request.files:
        return render_template("index.html", message="No file uploaded.")

    file = request.files['file']
    extracted_text = ""

    if file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        extracted_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif file.filename.endswith('.txt'):
        extracted_text = file.read().decode("utf-8")
    else:
        return render_template("index.html", message="Invalid file type. Please upload a PDF or TXT file.")

    if not extracted_text.strip():
        return render_template("index.html", message="File is empty or text could not be extracted.")

    message = predict_fake_or_real_email_content(extracted_text)
    return render_template("index.html", message=message)


@app.route('/predict', methods=['POST'])
def predict_url():
    url = request.form.get('url', '').strip()

    if not url.startswith(("http://", "https://")):
        return render_template("index.html",
                               message="⚠️ Invalid URL. Please include http:// or https://",
                               input_url=url)

    classification = url_detection(url)

    if classification is None:
        return render_template("index.html",
                               message="⚠️ The AI service is temporarily unavailable. Please try again in a few seconds.",
                               input_url=url)

    return render_template("index.html", input_url=url, predicted_class=classification)



if __name__ == '__main__':

    port = int(os.getenv("PORT", 8080))

    app.run(host='0.0.0.0', port=port, debug=False)
