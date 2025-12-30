from .acquisition import AcquisitionModule

from .acquisition import AcquisitionModule

from .visual_forgery import VisualForgeryModule
from .ocr_verification import OCRVerificationModule
from .biometrics import BiometricsModule
from .correlation import CorrelationModule
from .security_features import SecurityFeaturesModule
from .risk_scoring import RiskScoringModule
from .deployment import DeploymentModule

# Instantiate modules once (singleton-ish)
acquisition = AcquisitionModule()
visual_forgery = VisualForgeryModule()
ocr_verification = OCRVerificationModule()
biometrics = BiometricsModule()
correlation = CorrelationModule()
security = SecurityFeaturesModule()
risk_scoring = RiskScoringModule()
deployment = DeploymentModule()

def analyze_document(file_path: str, doc_type: str, config: dict = None):
    """
    Main entry point for the 8-Module Pipeline.
    Runs modules in logical order.
    Supports 'ablation' via config['enabled_modules'].
    """
    pipeline_results = []
    
    # Default: All enabled
    enabled = config.get("enabled_modules") if config else None
    
    def is_enabled(mod_name):
        return enabled is None or mod_name in enabled

    # 1. Acquisition
    if is_enabled("acquisition"):
        res_acq = acquisition.process(file_path)
        pipeline_results.append(res_acq)
    
    # 2. Visual Forgery
    if is_enabled("visual_forgery"):
        res_forgery = visual_forgery.process(file_path)
        pipeline_results.append(res_forgery)
    
    # 3. OCR (Extracts data needed for next steps)
    extracted_data = {}
    if is_enabled("ocr"):
        res_ocr = ocr_verification.process(file_path)
        pipeline_results.append(res_ocr)
        
        if res_ocr.get("status") == "success":
            # Simplified extraction from metadata for demo
            # In real OCR, we'd parse key-values here
            extracted_data["documentNumber"] = "X99282822" # Mock extraction
    
    # 4. Biometrics
    if is_enabled("biometrics"):
        res_bio = biometrics.process(file_path)
        pipeline_results.append(res_bio)
    
    # 5. Correlation (Uses extracted data)
    if is_enabled("correlation"):
        res_corr = correlation.process(file_path, extracted_data)
        pipeline_results.append(res_corr)
    
    # 6. Security Features
    if is_enabled("security"):
        res_sec = security.process(file_path, doc_type)
        pipeline_results.append(res_sec)
    
    # 7. Risk Scoring (Aggregates all)
    # Risk Engine always runs to aggregate whatever results exist
    risk_summary = risk_scoring.calculate_score(pipeline_results)
    
    # Log Final Decision
    import logging
    logging.info(f"Analysis Complete. ID: {extracted_data.get('documentNumber', 'Unknown')} | Score: {risk_summary['final_score']} | Risk: {risk_summary['risk_level']}")
    
    return {
        "pipeline_results": pipeline_results,
        "risk_summary": risk_summary,
        "deployment_info": deployment.get_config()
    }
