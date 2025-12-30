import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models import DocType

def test_model():
    print("Testing DocType logic...")
    try:
        # Test lowercase input
        d = DocType("id_proof")
        print(f"Input 'id_proof' -> {d} (value={d.value})")
        
        # Test uppercase input
        d2 = DocType("ID_PROOF")
        print(f"Input 'ID_PROOF' -> {d2} (value={d2.value})")
        
        # Test mixed
        d3 = DocType("Id_Proof")
        print(f"Input 'Id_Proof' -> {d3} (value={d3.value})")
        
    except Exception as e:
        print(f"Model Logic Error: {e}")

def read_log():
    print("\n--- Reading backend_error.log ---")
    try:
        if os.path.exists("backend_error.log"):
            with open("backend_error.log", "r") as f:
                print(f.read())
        else:
            print("Log file not found.")
    except Exception as e:
        print(f"Read Log Error: {e}")

if __name__ == "__main__":
    test_model()
    read_log()
