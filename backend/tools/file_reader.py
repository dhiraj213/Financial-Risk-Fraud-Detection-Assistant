import pandas as pd
import io
from fastapi import HTTPException

def read_file_content(file_bytes: bytes, filename: str) -> str:
    """
    Reads content from various file types (CSV, XLSX, TXT) and returns
    a standardized string representation for LLM consumption.
    """
    ext = filename.split('.')[-1].lower()
    
    try:
        if ext == 'csv':
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif ext in ('xlsx', 'xls'):
            df = pd.read_excel(io.BytesIO(file_bytes))
        elif ext == 'txt':
            # Read text file content directly
            return file_bytes.decode('utf-8')
        # elif ext == 'pdf':
            # NOTE: PDF parsing is complex. In a real app, use PyPDF2 or similar
            # For this MVP, we treat PDF content as a large text block.
            return f"PDF data (requires dedicated parser): {file_bytes[:200].decode('latin-1')}..."
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        # Convert DataFrame to a descriptive string for the LLM
        return f"File Type: {ext}\nColumns: {list(df.columns)}\n\nFirst 5 Rows:\n{df.head().to_string()}\n\nFull Data:\n{df.to_json(orient='records')}"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading {ext} file: {str(e)}")