import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Initialize Gemini
client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return "AI Medical Report Explainer Backend is Running!"


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # Check uploaded file
        if "file" not in request.files:
            return jsonify({"error": "No PDF uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Please upload a PDF file"}), 400

        # Read PDF
        reader = PdfReader(file)

        report_text = ""

        for page in reader.pages:
            report_text += page.extract_text() or ""

        if not report_text.strip():
            return jsonify({
                "error": "No readable text found. Please upload a text-based PDF."
            }), 400

        # Gemini prompt
        prompt = f"""
        You are a medical report explainer.

        Explain this medical report in very simple language.

        Provide:

        1. Report Summary
        2. Abnormal Values
        3. Possible Meaning
        4. Questions to Ask Doctor

        Do not provide a final diagnosis or prescribe medicines.
        Mention that a doctor should interpret the report.

        Medical Report:
        {report_text}
        """

        # Generate AI analysis
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return jsonify({
            "analysis": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)