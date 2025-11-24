import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/api/upload', formData);
      setJobId(res.data.job_id);
      setStatus("PROCESSING");
      pollStatus(res.data.job_id);
    } catch (err) {
      console.error(err);
      alert("Upload Failed");
      setLoading(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/status/${id}`);
        if (res.data.status === "COMPLETED") {
          setStatus("COMPLETED");
          setReport(res.data);
          setLoading(false);
          clearInterval(interval);
        } else if (res.data.status === "FAILED") {
          setStatus("FAILED");
          setLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        clearInterval(interval);
      }
    }, 2000);
  };

  return (
    <div className="App" style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🕵️‍♂️ AI Financial Fraud Agent</h1>
      
      <div style={{ marginBottom: "20px" }}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading} style={{ marginLeft: "10px" }}>
          {loading ? "Analyzing..." : "Start Analysis"}
        </button>
      </div>

      {status && <h3>Status: {status}</h3>}

      {report && (
        <div style={{ border: "1px solid #ddd", padding: "20px", borderRadius: "8px", textAlign: "left" }}>
          <h2>📊 Analysis Report</h2>
          <div style={{ backgroundColor: "#f9f9f9", padding: "10px", marginBottom: "10px" }}>
            <strong>🤖 AI Manager Summary:</strong>
            <p style={{ whiteSpace: "pre-wrap" }}>{report.manager_summary}</p>
          </div>

          <h3>Transaction Details</h3>
          <table border="1" cellPadding="5" style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Merchant</th>
                <th>Amount</th>
                <th>Risk Score</th>
                <th>Reason</th>
              </tr>
            </thead>
            <tbody>
              {report.transactions.map((tx, idx) => (
                <tr key={idx} style={{ backgroundColor: tx.is_anomaly ? "#ffcccc" : "white" }}>
                  <td>{tx.date}</td>
                  <td>{tx.merchant}</td>
                  <td>${tx.amount}</td>
                  <td>{tx.risk_score}</td>
                  <td>{tx.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;