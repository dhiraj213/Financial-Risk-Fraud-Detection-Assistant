from fastapi import HTTPException
import pandas as pd
import io
import uuid
from tools.anomaly_tool import detect_anomalies
from tools.llm_explainer import explain_risks
from tools.file_reader import read_file_content # New Import

# In-Memory Session Storage (For Demo)
session_store = {}

class CoordinatorAgent:
    def start_analysis(self, file_bytes: bytes, filename: str, user_prompt: str):
        job_id = str(uuid.uuid4())
        session_store[job_id] = {"status": "PROCESSING", "data": None}
        
        try:
            # 1. Parse File Content (Multi-Format)
            file_content_str = read_file_content(file_bytes, filename)
            
            # 2. Run LLM Initial Analysis (Using the prompt as guidance)
            # This is where the LLM would extract structured transactions based on the prompt
            # For this MVP, we will bypass LLM parsing and use Pandas for CSV/XLSX
            if "Full Data" in file_content_str:
                 df = pd.read_json(io.StringIO(file_content_str.split("Full Data:\n")[1]))
            else:
                 # If it's a TXT/PDF string, we can't easily convert to DF here.
                 # We will skip direct analysis and rely entirely on the LLM summary.
                 df = pd.DataFrame() 

            # 3. Anomaly Detection (Only if DataFrame parsing succeeded)
            if not df.empty:
                analyzed_data = detect_anomalies(df)
            else:
                analyzed_data = []
            
            # 4. Call Gemini (LLM) for Summary and Prompt-based analysis
            # We send the file content and the prompt for intelligent summarizing/parsing
            summary = explain_risks(analyzed_data, file_content_str, user_prompt)
            
            # 5. Save Result
            high_risk_count = sum(1 for x in analyzed_data if x.get('is_anomaly', False))
            
            result = {
                "job_id": job_id,
                "status": "COMPLETED",
                "total_transactions": len(analyzed_data) if not df.empty else "N/A",
                "high_risk_count": high_risk_count,
                "transactions": analyzed_data,
                "manager_summary": summary
            }
            session_store[job_id] = result
            
        except HTTPException as e:
            session_store[job_id] = {"status": "FAILED", "error": e.detail}
        except Exception as e:
            session_store[job_id] = {"status": "FAILED", "error": str(e)}
            
        return job_id

    def get_status(self, job_id: str):
        return session_store.get(job_id, {"status": "NOT_FOUND"})

    # New function for follow-up chat
    def handle_follow_up(self, job_id: str, user_query: str):
        # In a real system, we would retrieve the chat history from Firestore/DB,
        # and use the Gemini Chat API (model.start_chat()) to continue the conversation.
        
        report = session_store.get(job_id, {}).get("manager_summary", "No prior context.")
        
        # Simple LLM call for conversational response
        response = explain_risks(
            transactions=[], # No need to pass full data again
            file_content_summary=report, # Use prior summary as context
            user_prompt=user_query,
            is_follow_up=True
        )
        return {"response": response}