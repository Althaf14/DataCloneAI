class RiskScoringModule:
    # Max Penalty Caps (Weights)
    WEIGHTS = {
        "visual_forgery": 60,  # High
        "ocr_verification": 30, # Medium-High
        "biometrics": 20,       # Medium
        "security_features": 10 # Low-Medium
    }

    def __init__(self):
        self.name = "Centralized Risk Scoring"

    def calculate_score(self, pipeline_results):
        """
        Aggregates impacts from all modules, applies caps/weights, 
        and computes Final Score & Risk Level.
        """
        total_penalty = 0
        anomalies_summary = []
        
        for res in pipeline_results:
            mod_name = res.get("module", "").lower()
            impact = res.get("confidence_impact", 0)
            
            # Determine weight key
            w_key = None
            if "visual" in mod_name: w_key = "visual_forgery"
            elif "ocr" in mod_name or "text" in mod_name: w_key = "ocr_verification"
            elif "biometric" in mod_name: w_key = "biometrics"
            elif "security" in mod_name: w_key = "security_features"
            
            # Apply Cap
            if w_key:
                max_penalty = self.WEIGHTS[w_key]
                # impacts are negative, so we want max(impact, -max_penalty)
                # e.g. impact -100, max 60. we take -60.
                if impact < -max_penalty:
                    impact = -max_penalty
                    
            total_penalty += impact
            
            # Collect Anomalies for Summary
            if impact < 0:
                for anomaly in res.get("anomalies", []):
                    anomalies_summary.append(anomaly.get("description", "Unknown anomaly"))

        # Base 100
        final_score = 100 + total_penalty
        if final_score < 0: final_score = 0
        if final_score > 100: final_score = 100
        
        # Risk Level Classification
        if final_score < 50:
            risk_level = "CRITICAL" # Likely Fake
        elif final_score < 80:
            risk_level = "HIGH"    # Significant Anomalies
        elif final_score < 100:
            risk_level = "LOW"     # Minor Issues
        else:
            risk_level = "SAFE"    # Safe
            
        # Explanatory Summary
        summary = "Document appears authentic."
        if risk_level != "SAFE":
            unique_anomalies = list(set(anomalies_summary))
            if len(unique_anomalies) > 3:
                reasons = ", ".join(unique_anomalies[:3]) + f", and {len(unique_anomalies)-3} more issues."
            else:
                reasons = ", ".join(unique_anomalies)
            summary = f"{risk_level} RISK detected due to: {reasons}"

        return {
            "final_score": round(final_score, 2),
            "risk_level": risk_level,
            "summary": summary,
            "breakdown": anomalies_summary
        }
