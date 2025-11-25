import google.generativeai as genai
import os
from typing import List, Optional

# TODO: Replace with your actual key or use os.getenv("GOOGLE_API_KEY")
API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE") 

genai.configure(api_key=API_KEY)

def explain_risks(
    transactions: List[dict], 
    file_content_summary: Optional[str] = None, 
    user_prompt: Optional[str] = None, 
    is_follow_up: bool = False
) -> str:
    """
    Sends flagged transactions to Gemini to generate a manager summary.
    """
    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return "⚠️ Gemini API Key missing. Please set GOOGLE_API_KEY."

    # --- 💡 FIX IS HERE: Using gemini-2.5-flash for broader compatibility and speed ---
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Context Engineering: Summarizing data for the prompt
    high_risk_tx = [t for t in transactions if t.get('risk_score', 0) > 50]
    
    if not high_risk_tx:
        return "No high-risk transactions detected. Operations look normal."

    # Extract only necessary data for the prompt to save context window space
    prompt_data = [
        {
            "id": t.get("id"),
            "amount": t.get("amount"),
            "merchant": t.get("merchant"),
            "risk_score": t.get("risk_score"),
            "reason_flags": t.get("reason")
        } 
        for t in high_risk_tx
    ]

    prompt = f"""
    You are a Financial Fraud Analyst. Analyze these high-risk transactions:
    {prompt_data}
    
    1. Summarize the suspicious patterns (e.g., 'High amount transactions focused on electronics/unknown merchants').
    2. Give a definitive risk assessment (Low/Medium/High).
    3. Suggest immediate actions for the manager (e.g., 'Suspend card and contact user').
    Keep the response professional, concise, and under 100 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Re-run the analysis to see if the error is gone
        return f"Error generating explanation: {str(e)}"