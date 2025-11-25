# Financial-Risk-Fraud-Detection-Assistant
---
Agents Intensive - Capstone Project
This Capstone Project is part of the 5-Day AI Agents Intensive Course with Google (Nov 10 - 14, 2025)

---
An AI-powered assistant designed to analyze transactional data , detect anomalies using predefined rules, and generate concise, professional risk summaries using Google's Gemini Large Language Model.

The project is built on a robust, service-oriented architecture, featuring a FastAPI backend and a React.js frontend.

---
✨ Key Features
---

This assistant is engineered for maximum flexibility and analytical depth:

Multi-Format Data Ingestion: Supports upload and parsing of data:

Intelligent Risk Assessment: Uses a specialized Python Anomaly Tool for rule-based detection, followed by the Gemini LLM for high-level risk summarization.

Robust Backend Design: Column name standardization and error handling ensure the system remains stable regardless of minor casing variations in uploaded data (e.g., handling Amount, amount, or AMOUNT).

---

🧱 Architecture Overview
---
The system follows a standard microservice-like pattern with a clean separation of concerns.

Backend (Python/FastAPI)
The brain of the operation, structured around a central CoordinatorAgent that orchestrates all steps:

Agents (agents/):
coordinator.py: The control hub. Manages the workflow: determines if input is a File or a Database Query, calls the correct tool, runs anomaly detection, and calls the LLM for the final summary.

Tools (tools/):
file_reader.py: Handles parsing of uploaded files (CSV, XLSX, PDF, TXT) into a standard format.

db_connector.py: Executes SQL queries and fetches data from a mock database (can be adapted for any SQL database using SQLAlchemy).

anomaly_tool.py: Runs rule-based detection (Z-Score, high value, duplicate merchant) and flags transactions.

llm_explainer.py: Interacts with the Gemini API to turn structured anomaly data into a conversational, manager-ready report.

Frontend (React/Web)
Handles the user interface, file upload, chat interaction, and state management. Critically, it manages Firebase integration for authentication and persistence.

---
⚙️ Setup and Installation
---
Follow these steps to get the Financial Assistant running locally.

1. Set up the Backend

Navigate to the backend directory:

cd backend

Install Dependencies: Install all required Python packages, including FastAPI, Pandas, PyPDF2, and SQLAlchemy.

pip install -r requirements.txt
pip install numpy # Ensure numpy is explicitly installed

Set up the Gemini API Key:
Create a .env file in the backend directory and add your Gemini API Key.

# .env file in the backend directory
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"

Run the Backend Server:

python api/main.py

The server should start on http://0.0.0.0:8000.

2. Run the Frontend

The frontend is assumed to be running on http://localhost:3000 (typical for React development) and automatically connects to the backend on port 8000.

---
🚀 Usage
---

File Analysis 

Upload your financial data file (e.g., test_high_value_fraud.csv).

The system parses the file, detects anomalies, and provides a summary.

