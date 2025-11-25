from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.coordinator import CoordinatorAgent
import uvicorn
import fastapi

app = FastAPI()

# Allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...), 
    prompt: str = Form("Analyze all transactions for anomalies.") # New prompt field
):
    valid_extensions = ('.csv', '.xlsx', '.xls', '.txt', '.pdf')
    if not file.filename.lower().endswith(valid_extensions):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please use CSV, XLSX, TXT, or PDF.")
    
    content = await file.read()
    
    # Pass prompt to the coordinator
    job_id = coordinator.start_analysis(content, file.filename, prompt)
    return {"job_id": job_id, "message": "Analysis started"}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    return coordinator.get_status(job_id)

@app.post("/api/chat/{job_id}")
async def post_follow_up(job_id: str, query: dict):
    """Handle conversational follow-up questions."""
    user_query = query.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required.")
    
    # Handle follow-up chat logic
    response = coordinator.handle_follow_up(job_id, user_query)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)