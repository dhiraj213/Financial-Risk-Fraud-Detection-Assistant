import pandas as pd
import io
import uuid
from tools.anomaly_tool import detect_anomalies
from tools.llm_explainer import explain_risks

# In-Memory Session Storage (For Demo)
session_store = {}

class CoordinatorAgent:
    def start_analysis(self, file_bytes: bytes, filename: str):
        job_id = str(uuid.uuid4())
        session_store[job_id] = {"status": "PROCESSING", "data": None}
        
        # Async simulation (In real app, use Celery/BackgroundTasks)
        try:
            # 1. Parse File
            df = pd.read_csv(io.BytesIO(file_bytes))
            
            # 2. Run Tools
            analyzed_data = detect_anomalies(df)
            
            # 3. Call Gemini (LLM)
            summary = explain_risks(analyzed_data)
            
            # 4. Save Result
            high_risk_count = sum(1 for x in analyzed_data if x['is_anomaly'])
            
            result = {
                "job_id": job_id,
                "status": "COMPLETED",
                "total_transactions": len(analyzed_data),
                "high_risk_count": high_risk_count,
                "transactions": analyzed_data,
                "manager_summary": summary
            }
            session_store[job_id] = result
            
        except Exception as e:
            session_store[job_id] = {"status": "FAILED", "error": str(e)}
            
        return job_id

    def get_status(self, job_id: str):
        return session_store.get(job_id, {"status": "NOT_FOUND"})