import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import cv2
    print(f"OpenCV loaded successfully! Version: {cv2.__version__}")
except ImportError as e:
    print(f"Failed to load OpenCV: {e}")
except ModuleNotFoundError as e:
    print(f"OpenCV not found: {e}")
