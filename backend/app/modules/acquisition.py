import numpy as np
from PIL import Image, ExifTags
import os
import logging

class AcquisitionModule:
    def __init__(self):
        self.name = "Document Acquisition & Pre-Processing"

    def process(self, file_path):
        """
        Standardizes input, removes glare, extracts metadata using Pillow and Numpy.
        """
        results = {
            "module": self.name,
            "status": "success",
            "confidence_impact": 0, # Start neutral
            "signal_strength": 0.0,
            "metadata": {},
            "anomalies": []
        }

        try:
            # 1. Read Image
            if not os.path.exists(file_path):
                results["status"] = "error"
                results["error"] = "File not found"
                results["confidence_impact"] = -100
                return results

            try:
                pil_img = Image.open(file_path)
                pil_img.load() # Verify integrity
            except Exception:
                results["status"] = "error"
                results["error"] = "Invalid image format"
                results["confidence_impact"] = -100
                return results

            # 2. Extract basic metadata (resolution, etc)
            w, h = pil_img.size
            mode = pil_img.mode
            results["metadata"]["resolution"] = f"{w}x{h}"
            results["metadata"]["channels"] = len(mode)
            
            # 3. Glare Detection (Histogram Analysis)
            # Convert to grayscale equivalent (Luminance)
            if mode != 'L':
                gray_img = pil_img.convert('L')
            else:
                gray_img = pil_img
            
            # Convert to numpy array for fast processing
            img_array = np.array(gray_img)
            
            # Heuristic: Pixels > 240 considered 'glare' or overexposed
            bright_pixels = np.sum(img_array > 240)
            total_pixels = w * h
            bright_ratio = bright_pixels / total_pixels
            
            results["metadata"]["glare_ratio"] = float(round(bright_ratio, 4))
            results["signal_strength"] = float(round(bright_ratio, 4)) # Signal is the glare amount

            if bright_ratio > 0.05: # > 5% glare is significant
                penalty = -10
                if bright_ratio > 0.2:
                    penalty = -30
                
                results["confidence_impact"] += penalty
                results["anomalies"].append({
                    "region": "global",
                    "description": f"High glare/overexposure detected ({bright_ratio*100:.1f}%) - might affect OCR",
                    "score": 0.0 # Legacy field
                })

            # Check EXIF
            exif_data = pil_img._getexif()
            if exif_data:
                results["metadata"]["exif_present"] = True
                # Optional: Extract specific keys like Software or DateTime
                software = exif_data.get(0x0131) # 305 -> 0x0131
                if software:
                    results["metadata"]["software"] = str(software)
                    # Detect editing software signatures
                    if "photoshop" in str(software).lower() or "gimp" in str(software).lower():
                        results["confidence_impact"] += -20
                        results["anomalies"].append({
                            "region": "metadata",
                            "description": f"Editing software signature detected: {software}",
                            "score": 0.5
                        })
            else:
                results["metadata"]["exif_present"] = False
                results["confidence_impact"] += -5 # Slight uncertainty penalty for stripping EXIF

        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            results["confidence_impact"] = -5
            logging.error(f"Acquisition Error: {e}")

        return results
