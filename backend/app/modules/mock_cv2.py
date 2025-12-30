import logging
import numpy as np

class MockCV2:
    # Constants
    IMWRITE_JPEG_QUALITY = 1
    COLOR_BGR2GRAY = 6
    THRESH_BINARY = 0
    THRESH_BINARY_INV = 1
    RETR_EXTERNAL = 0
    CHAIN_APPROX_SIMPLE = 1
    ROTATE_90_CLOCKWISE = 0
    ROTATE_180 = 1
    ROTATE_90_COUNTERCLOCKWISE = 2
    
    class _Data:
        haarcascades = ""
    data = _Data()

    def __getattr__(self, name):
        def _dummy(*args, **kwargs):
            logging.warning(f"MockCV2 method called: {name}")
            return None
        return _dummy

    def imread(self, *args, **kwargs):
        # Return a black image 100x100 RGB
        return np.zeros((100, 100, 3), dtype=np.uint8)
    
    def imwrite(self, *args, **kwargs):
        return True

    def cvtColor(self, *args, **kwargs):
        # Return black image grayscale
        return np.zeros((100, 100), dtype=np.uint8)
    
    def threshold(self, *args, **kwargs):
        # ret, mask
        return 0, np.zeros((100, 100), dtype=np.uint8)

    def findContours(self, *args, **kwargs):
        # contours, hierarchy
        return [], None
    
    def contourArea(self, *args, **kwargs):
        return 0.0
        
    def boundingRect(self, *args, **kwargs):
        return 0,0,0,0
    
    def Canny(self, *args, **kwargs):
        return np.zeros((100, 100), dtype=np.uint8)
    
    def absdiff(self, *args, **kwargs):
        return np.zeros((100, 100, 3), dtype=np.uint8)
        
    def rotate(self, img, code):
        return img

    class CascadeClassifier:
        def __init__(self, *args, **kwargs):
            pass
        def detectMultiScale(self, *args, **kwargs):
            return []
            
    class QRCodeDetector:
        def __init__(self, *args, **kwargs):
            pass
        def detectAndDecode(self, *args, **kwargs):
            return None, None, None
