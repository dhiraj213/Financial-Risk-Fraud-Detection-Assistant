import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Importing the new CSS

// Base URL for the FastAPI backend
const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState("IDLE");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setReport(null);
    setError(null);
    setStatus("READY");
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setStatus("UPLOADING...");

    const formData = new FormData();
    formData.append('file', file);

    try {
      // 1. Start Analysis (Long-Running Ops)
      const res = await axios.post(`${API_BASE_URL}/api/upload`, formData);
      
      const newJobId = res.data.job_id;
      setJobId(newJobId);
      setStatus("PROCESSING");
      
      // 2. Start Polling (Observability)
      pollStatus(newJobId);

    } catch (err) {
      console.error("Upload Failed:", err);
      setError(err.response?.data?.detail || "Could not connect to Agent Backend.");
      setStatus("FAILED");
      setLoading(false);
    }
  };

  const pollStatus = (id) => {
    const interval = setInterval(async () => {
      try {
        // Fetch Status (Sessions & State Management)
        const res = await axios.get(`${API_BASE_URL}/api/status/${id}`);
        const currentStatus = res.data.status;
        setStatus(currentStatus);

        if (currentStatus === "COMPLETED") {
          setReport(res.data);
          setLoading(false);
          clearInterval(interval);
        } else if (currentStatus === "FAILED") {
          setError(res.data.error || "Analysis failed due to an internal error.");
          setLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        // Use exponential backoff here in a production environment
        clearInterval(interval);
        console.error("Polling error:", err);
        setError("Network error while polling job status.");
        setStatus("FAILED");
        setLoading(false);
      }
    }, 2000);

    // Store the interval ID to clear it later if needed (e.g., component unmounts)
    return () => clearInterval(interval);
  };
  
  // Custom Status Display based on state
  const getStatusText = () => {
    switch (status) {
      case "IDLE": return "Upload a CSV file to begin risk analysis.";
      case "READY": return "File ready for analysis. Click 'Start'.";
      case "UPLOADING...": return "File is being uploaded...";
      case "PROCESSING": return `Analyzing transactions... (Job ID: ${jobId})`;
      case "COMPLETED": return `Analysis Complete! Detected ${report?.high_risk_count || 0} anomalies.`;
      case "FAILED": return `Analysis FAILED. See error below.`;
      default: return `Current Status: ${status}`;
    }
  }

  return (
    <div className="App">
      <h1>🕵️‍♂️ AI Financial Fraud Agent</h1>
      
      <div className="input-container">
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button 
          onClick={handleUpload} 
          disabled={loading || !file} 
          title={!file ? "Select a file first" : ""}
        >
          {loading ? "Analyzing..." : "Start Analysis"}
        </button>
      </div>

      <div className="status-info">
        <p>Status: <span style={{color: error ? '#ff7b72' : status === 'COMPLETED' ? '#3fb950' : '#e3b341'}}>{getStatusText()}</span></p>
        {error && <p style={{color: '#ff7b72', marginTop: '10px'}}>Error: {error}</p>}
      </div>

      {report && (
        <div className="report-card">
          <h2><span role="img" aria-label="report">📊</span> Analysis Report</h2>
          
          {/* AI Manager Summary */}
          <div className="summary-box">
            <strong><span role="img" aria-label="robot">🤖</span> AI Manager Summary:</strong>
            <p style={{ whiteSpace: "pre-wrap", marginTop: '5px', lineHeight: '1.6' }}>{report.manager_summary}</p>
          </div>

          {/* Transaction Details Table */}
          <h3><span role="img" aria-label="list">📋</span> Transaction Details ({report.total_transactions} items)</h3>
          <table className="transaction-table">
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
                <tr 
                  key={idx} 
                  className={tx.is_anomaly ? "anomaly-row" : ""}
                >
                  <td>{tx.date}</td>
                  <td>{tx.merchant}</td>
                  <td>${tx.amount.toFixed(2)}</td>
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