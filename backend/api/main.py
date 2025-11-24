from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agents.coordinator import CoordinatorAgent
import uvicorn
import os

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
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
    
    content = await file.read()
    job_id = coordinator.start_analysis(content, file.filename)
    return {"job_id": job_id, "message": "Analysis started"}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    return coordinator.get_status(job_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)