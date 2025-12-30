import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
from PIL import Image
import numpy as np
import scipy.ndimage

class CNNForgeryDetector:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = None
        self._load_model()
        
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def _load_model(self):
        try:
            # We use ResNet18 for efficiency
            # Weights=DEFAULT loads IMAGENET1K_V1
            self.model = resnet18(weights=ResNet18_Weights.DEFAULT)
            
            # We only need the feature extractor stages, up to layer 4
            # We can cut off the avgpool and fc layer.
            self.model = nn.Sequential(*list(self.model.children())[:-2])
            
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            print(f"Failed to load ResNet Model: {e}")
            self.model = None

    def detect(self, image_path):
        """
        Runs the image through the CNN backbone.
        Returns:
            heatmap (numpy 2D): 0-1 values indicating anomaly likelihood.
            score (float): Global anomaly score.
        """
        if not self.model:
            return None, 0.0

        try:
            img = Image.open(image_path).convert('RGB')
            # Save original size for upsampling later
            orig_w, orig_h = img.size
            
            input_tensor = self.preprocess(img).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                # Forward pass
                # Output shape: [1, 512, 7, 7] for ResNet18 with 224x224 input
                features = self.model(input_tensor)
                
            # --- Anomaly Calculation ---
            # Hypothesis: Spliced regions often have different texture statistics/noise patterns.
            # In deep feature space, this might manifest as high variance or unexpected activations
            # relative to the rest of the image.
            
            # Simplified Approach: Calculate "saliency" or activation magnitude deviation.
            # 1. Compute mean activation map across channels: [1, 7, 7]
            # features_sq = features.pow(2).mean(1).squeeze(0) # [7, 7] Energy
            
            # Better approach for "Anomaly":
            # Compute distance of each spatial vector from the global mean vector of the image.
            # 1. Flatten spatial dims: [1, 512, 49]
            b, c, h, w = features.shape
            features_flat = features.view(c, -1).permute(1, 0) # [49, 512]
            
            # 2. Compute Global Mean Vector (Prototype of the image style)
            # We exclude the current vector from its own mean calculation to prevent cheating? 
            # No, simple mean is fine for global style.
            global_mean = features_flat.mean(0) # [512]
            
            # 3. Compute Distance (Euclidean) of each patch to the global mean
            # Patches that deviate significantly from the global "style" are suspects.
            # dist shape: [49]
            dists = torch.norm(features_flat - global_mean, dim=1)
            
            # 4. Reshape back to [7, 7]
            anomaly_map = dists.view(h, w).cpu().numpy()
            
            # 5. Upsample to original image size
            # We use scipy zoom or simple resize
            # Normalize to 0-1 first
            min_val = anomaly_map.min()
            max_val = anomaly_map.max()
            if max_val - min_val > 1e-5:
                anomaly_map = (anomaly_map - min_val) / (max_val - min_val)
            else:
                anomaly_map = np.zeros_like(anomaly_map)
                
            # Resize
            heatmap = Image.fromarray((anomaly_map * 255).astype(np.uint8), mode='L')
            heatmap = heatmap.resize((orig_w, orig_h), Image.BICUBIC)
            
            # Global Score: Max anomaly or Mean of top 10% anomalies
            # High local variance is key.
            global_score = float(np.mean(np.sort(anomaly_map.flatten())[-5:])) # Top 5 pixels average in 7x7 grid
            
            return np.array(heatmap) / 255.0, global_score

        except Exception as e:
            print(f"CNN Detection Error: {e}")
            return None, 0.0
