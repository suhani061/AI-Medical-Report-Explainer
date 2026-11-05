import os
import time
from google.genai import errors
from google import genai
from pypdf import PdfReader
from dotenv import load_dotenv

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

# Read medical report PDF
reader = PdfReader("report.pdf")

report_text = ""

for page in reader.pages:
    report_text += page.extract_text() or ""

print("Extracted Report Text:")
print(report_text)

print("\nTotal characters extracted:", len(report_text))

# Create prompt
prompt = f"""
You are a medical report explainer.

Explain this medical report in very simple language.

Provide:

1. Report Summary
2. Abnormal Values
3. Possible Meaning
4. Questions to Ask Doctor

Important:
- Explain medical terms in simple language.
- Do not give a final diagnosis.
- Do not recommend medicines.
- Mention that the report should be discussed with a qualified doctor.

Medical Report:

{report_text}
"""

# Generate AI response
response = None

for attempt in range(3):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        break

    except errors.APIError as e:
        if e.code not in [429, 500, 502, 503, 504]:
            raise

        if attempt == 2:
            raise

        wait_time = 2 ** (attempt + 1)
        print(f"Gemini temporarily unavailable. Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

# Display result
print("\nAI MEDICAL REPORT ANALYSIS\n")

print(response.text)

print("\n___________________________________")
