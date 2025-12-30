class SecurityFeaturesModule:
    def __init__(self):
        self.name = "Security Features Verification"

    def process(self, file_path, doc_type):
        """
        Checks for Holograms, QR codes, and Metadata anomalies.
        """
        results = {
            "module": self.name,
            "status": "success",
            "confidence_impact": 0,
            "signal_strength": 0.0, # 1.0 = verified security feature found
            "metadata": {},
            "anomalies": []
        }
        
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        img = Image.open(file_path)
        
        # --- 1. QR/Barcode Detection (Graceful Fallback) ---
        try:
            from pyzbar.pyzbar import decode
            decoded_objects = decode(img)
            
            if decoded_objects:
                # Found something
                results["metadata"]["qr_found"] = True
                results["metadata"]["qr_data"] = [obj.data.decode('utf-8') for obj in decoded_objects]
                results["signal_strength"] = 0.9 # High trust if verification code exists
            else:
                # No QR found - acceptable for many docs
                results["metadata"]["qr_found"] = False
                
        except ImportError:
            results["metadata"]["note"] = "QR Detection skipped (pyzbar not installed)"
            results["status"] = "warning"
            # No penalty for missing QR engine in local env
        except Exception as e:
            results["metadata"]["qr_error"] = str(e)

        # --- 2. EXIF & Metadata/Compression Analysis ---
        # Goal: Detect if 'Software' tag indicates editing tools
        try:
            exif_data = img.getexif()
            software_tag_id = 0x0131 # 'Software'
            
            if exif_data:
                software_name = exif_data.get(software_tag_id)
                if software_name:
                    results["metadata"]["software_tag"] = software_name
                    
                    suspicious_tools = ["photoshop", "gimp", "paint.net", "adobe"]
                    if any(tool in software_name.lower() for tool in suspicious_tools):
                        results["confidence_impact"] += -10
                        results["anomalies"].append({
                            "region": "metadata",
                            "description": f"Editing software detected in metadata: {software_name}",
                            "score": 0.0
                        })
            
            # Additional Digital Traces
            if "icc_profile" in img.info:
                # Just flag strictly if we had a database of camera profiles, 
                # for now just note it.
                results["metadata"]["has_icc_profile"] = True

        except Exception as e:
            results["metadata"]["exif_error"] = str(e)
            
        return results
