import google.generativeai as genai
import os
from typing import List

# TODO: Replace with your actual key or use os.getenv("GOOGLE_API_KEY")
API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE") 

genai.configure(api_key=API_KEY)

def explain_risks(transactions: List[dict]) -> str:
    """
    Sends flagged transactions to Gemini to generate a manager summary.
    """
    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return "⚠️ Gemini API Key missing. Please set GOOGLE_API_KEY."

    model = genai.GenerativeModel('gemini-pro')
    
    # Context Engineering: Summarizing data for the prompt
    high_risk_tx = [t for t in transactions if t['risk_score'] > 50]
    
    if not high_risk_tx:
        return "No high-risk transactions detected. Operations look normal."

    prompt = f"""
    You are a Financial Fraud Analyst. Analyze these high-risk transactions:
    {high_risk_tx}
    
    1. Summarize the suspicious patterns.
    2. Give a risk assessment (Low/Medium/High).
    3. Suggest immediate actions for the manager.
    Keep it professional and concise.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating explanation: {str(e)}"