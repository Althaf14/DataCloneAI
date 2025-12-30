import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models import DocType

try:
    print(f"DocType defined: {list(DocType)}")
    
    val = "id_proof"
    print(f"Testing DocType('{val}')...")
    dt = DocType(val)
    print(f"Success: {dt}")

    val_upper = "ID_PROOF"
    print(f"Testing DocType('{val_upper}')...")
    dt2 = DocType(val_upper)
    print(f"Success: {dt2}")
    
    val_mixed = "Id_Proof"
    print(f"Testing DocType('{val_mixed}')...")
    dt3 = DocType(val_mixed)
    print(f"Success: {dt3}")

except Exception as e:
    print(f"Error: {e}")
