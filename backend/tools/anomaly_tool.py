import pandas as pd

def detect_anomalies(df: pd.DataFrame):
    """
    Simple Z-score based anomaly detection using Pandas.
    """
    # Simulate risk scoring logic
    results = []
    mean_amount = df['amount'].mean()
    
    for _, row in df.iterrows():
        risk_score = 0
        reason = []
        
        # Rule 1: High Amount
        if row['amount'] > (mean_amount * 2):
            risk_score += 40
            reason.append("Amount unusually high")
            
        # Rule 2: Round Numbers (often suspicious)
        if row['amount'] % 1000 == 0 and row['amount'] > 5000:
            risk_score += 30
            reason.append("Large round number transaction")
            
        # Rule 3: Random Chaos (Demo purpose)
        if row['merchant'].lower() == "unknown":
            risk_score += 50
            reason.append("Unknown merchant")

        results.append({
            **row.to_dict(),
            "risk_score": min(risk_score, 100),
            "is_anomaly": risk_score > 50,
            "reason": ", ".join(reason) if reason else "Normal"
        })
        
    return results