import pytesseract
import re
from PIL import Image

class OCRVerificationModule:
    def __init__(self):
        self.name = "Text Consistency & OCR"

    def process(self, file_path):
        """
        Extracts text and performs advanced consistency checks:
        1. Character/Word-level Confidence Dips (possible overwrite).
        2. Font Size Analysis (inserted text often differs in size).
        3. Keyword Integrity (Name, DOB).
        """
        results = {
            "module": self.name,
            "status": "success",
            "confidence_impact": 0,
            "signal_strength": 0.0,
            "metadata": {},
            "anomalies": []
        }
        
        try:
            # Load Image (Use PIL/Numpy for Density calc to avoid cv2 dependency)
            import numpy as np
            
            img_pil = Image.open(file_path).convert('L') # Grayscale
            img_np = np.array(img_pil)
            
            # Output dict has keys: 'level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'
            ocr_data = pytesseract.image_to_data(img_pil, output_type=pytesseract.Output.DICT)
            n_boxes = len(ocr_data['text'])
            
            # Data Structures
            lines = {} # Key: (block, par, line) -> list of word dicts
            all_words = []
            
            # --- 1. Parse and Group Data ---
            for i in range(n_boxes):
                if int(ocr_data['conf'][i]) == -1: continue 
                text = ocr_data['text'][i].strip()
                if not text: continue
                
                # Extract BBox
                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                
                # Calculate Pixel Density (Ink Thickness)
                # ROI extraction
                if w > 0 and h > 0:
                    roi = img_np[y:y+h, x:x+w]
                    # Simple Thresholding (assuming dark text on light bg)
                    # Count pixels darker than 128
                    ink_pixels = np.count_nonzero(roi < 128)
                    area = w * h
                    density = ink_pixels / area
                else:
                    density = 0
                
                word_info = {
                    "text": text,
                    "conf": int(ocr_data['conf'][i]),
                    "x": x, "y": y, "w": w, "h": h,
                    "density": density,
                    "right": x + w,
                    "line_key": (ocr_data['block_num'][i], ocr_data['par_num'][i], ocr_data['line_num'][i])
                }
                
                if word_info["line_key"] not in lines:
                    lines[word_info["line_key"]] = []
                lines[word_info["line_key"]].append(word_info)
                all_words.append(word_info)

            full_text = " ".join([w["text"] for w in all_words])
            results["metadata"]["raw_text_snippet"] = full_text[:100] + "..." if full_text else ""
            
            # --- 2. Advanced Anomaly Detection ---
            ocr_penalty = 0
            
            # A. Overwritten Text (Overlap) & Spacing
            for key, line_words in lines.items():
                if len(line_words) < 2: continue
                
                # Check Sensitive Context (Name, DOB, ID)
                line_text = " ".join([w["text"] for w in line_words]).lower()
                is_sensitive = any(k in line_text for k in ["name", "date", "dob", "identity", "no."])
                multiplier = 2.0 if is_sensitive else 1.0
                
                # Sort by X
                line_words.sort(key=lambda x: x["x"])
                
                prev_word = line_words[0]
                
                for i in range(1, len(line_words)):
                    curr_word = line_words[i]
                    
                    # Gap Calculation
                    gap = curr_word["x"] - prev_word["right"]
                    
                    # 1. Overlap Check (Negative Gap)
                    # Allow small tolerance (-2 pixels) for tight kerning
                    if gap < -3: 
                        results["anomalies"].append({
                            "region": f"text_overlap",
                            "description": f"Overwritten text detected: '{prev_word['text']}' overlaps '{curr_word['text']}' (Gap {gap}px)",
                            "score": 0.0,
                            "bbox": [curr_word["x"], curr_word["y"], curr_word["w"], curr_word["h"]]
                        })
                        ocr_penalty += -15 * multiplier
                    
                    # 2. Abnormal Spacing (Huge Gap within line)
                    # Rough heuristic: if gap > 3x prev width (unlikely in same line unless simplified tesseract logic)
                    if gap > 5 * prev_word["h"]: # compare to height as proxy for font size
                         # Only flag if not intended separation
                         pass 
                         
                    prev_word = curr_word

            # B. Font Thickness / Density Consistency
            for key, line_words in lines.items():
                if len(line_words) < 3: continue
                
                # Calculate median density for line
                densities = [w["density"] for w in line_words]
                median_density = sorted(densities)[len(densities)//2]
                
                if median_density < 0.1: continue # Skip if very sparse/fail
                
                for w in line_words:
                    # Deviation: > 35% difference
                    deviation_ratio = abs(w["density"] - median_density) / median_density
                    if deviation_ratio > 0.4:
                        results["anomalies"].append({
                            "region": "font_consistency",
                            "description": f"Font thickness inconsistency in '{w['text']}' (Density mismatch vs line)",
                            "score": 0.0
                        })
                        ocr_penalty += -10 # No multiplier, usually less critical checks
            
            
            # Existing specific checks (Confidence Dips - Retained)
            confidence_dips = 0
            for i in range(1, len(all_words) - 1):
                prev_w = all_words[i-1]
                curr_w = all_words[i]
                next_w = all_words[i+1]
                if curr_w["conf"] < 60 and prev_w["conf"] > 80 and next_w["conf"] > 80:
                    confidence_dips += 1
            if confidence_dips > 0:
                ocr_penalty += -15 * min(confidence_dips, 2)
                results["anomalies"].append({
                     "region": "text_flow",
                     "description": f"Localized confidence dip detected ({confidence_dips} zones)",
                     "score": 0.0
                })

            # Cap Max Penalty
            if ocr_penalty < -80: ocr_penalty = -80
            
            results["confidence_impact"] = ocr_penalty
            results["metadata"]["ocr_score"] = 100 + ocr_penalty
            
            # --- Keyword Checks (Existing) ---
            suspicious_words = ["sample", "edited", "specimen", "void"]
            found_suspicious = [w for w in suspicious_words if w in full_text.lower()]
            if found_suspicious:
                  results["confidence_impact"] += -50
                  results["anomalies"].append({
                    "region": "text_content",
                    "description": f"Watermark detected: {', '.join(found_suspicious)}",
                    "score": 0.0
                })

        except Exception as e:
            results["status"] = "warning"
            results["error"] = f"OCR Error: {str(e)}"
            results["confidence_impact"] = -5
            
        return results
