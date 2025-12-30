import subprocess
import os

if not os.path.exists("test.txt"):
    with open("test.txt", "w") as f:
        f.write("test content")

url = "http://127.0.0.1:8000/api/documents/upload"
try:
    print(f"Testing URL: {url}")
    # Using 'curl' assuming it's in PATH (Windows usually has it)
    # If not, we might see error
    res = subprocess.run(["curl", "-v", "-X", "POST", "-F", "file=@test.txt", "-F", "doc_type=id_proof", url], capture_output=True, text=True)
    print("--- STDOUT ---")
    print(res.stdout)
    print("--- STDERR ---")
    print(res.stderr)
except Exception as e:
    print(f"Script Error: {e}")
