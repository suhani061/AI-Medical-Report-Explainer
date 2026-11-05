import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";
import jsPDF from "jspdf";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setResult("");

      const response = await axios.post(
        "http://127.0.0.1:5000/analyze",
        formData
      );

      setResult(response.data.analysis);
    } catch (error) {
      setResult(
        error.response?.data?.error || "Something went wrong!"
      );
    } finally {
      setLoading(false);
    }
  };

  // Download analysis
  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.setFontSize(18);
    doc.text("AI Medical Report Analysis", 20, 20);

    doc.setFontSize(11);

    const lines = doc.splitTextToSize(result, 170);

    let y = 35;

    lines.forEach((line) => {
      if (y > 275) {
        doc.addPage();
        y = 20;
      }

      doc.text(line, 20, y);
      y += 7;
    });

    doc.save("Medical_Report_Analysis.pdf");
  };
  const downloadAnalysis = () => {
    if (!result) return;

    const blob = new Blob([result], {
      type: "text/plain",
    });

    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "Medical_Report_Analysis.txt";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="container">

      <h1>AI Medical Report Explainer</h1>

      <p>
        Understand your medical reports in simple language
        with the help of AI.
      </p>

      <div className="upload-box">

        <h2>Upload Your Medical Report</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        {file && <p>Selected: {file.name}</p>}

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Analysing..." : "Analyse Report"}
        </button>

      </div>

      {result && (
        <div className="result-box">

          <h2>Analysis Result</h2>

          <div className="markdown-content">
            <ReactMarkdown>{result}</ReactMarkdown>
          </div>

          <button
            className="download-btn"
            onClick={downloadAnalysis}
          >
            Download Analysis
          </button>

          <button
            className="download-btn"
            onClick={downloadPDF}
          >
            Download as PDF
          </button>

        </div>
      )}

      <p className="disclaimer">
        Disclaimer: This tool is for educational purposes only.
        Always consult a qualified doctor for medical advice.
      </p>

    </div>
  );
}

export default App; 