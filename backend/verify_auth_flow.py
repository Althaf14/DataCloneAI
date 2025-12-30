import requests
import sys
import uuid

BASE_URL = "http://localhost:8000"

def run_verification():
    # 1. Register
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "testpassword"
    print(f"Registering user: {username}")
    
    try:
        resp = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
        if resp.status_code == 200:
             print("User already exists? Login success.")
        else:
             # Try register
             reg_resp = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})
             if reg_resp.status_code != 200:
                 print(f"Registration failed: {reg_resp.text}")
                 return False
             user_data = reg_resp.json()
             print(f"Registered user ID: {user_data.get('id')}")

        # 2. Login
        print("Logging in...")
        login_resp = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
        if login_resp.status_code != 200:
             print(f"Login failed: {login_resp.text}")
             return False
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful, token received.")

        # 3. Upload Document
        print("Uploading document...")
        files = {'file': ('test_doc.txt', 'This is a test document content.', 'text/plain')}
        upload_resp = requests.post(f"{BASE_URL}/api/documents/upload", headers=headers, files=files)
        
        if upload_resp.status_code != 200:
            print(f"Upload failed: {upload_resp.text}")
            return False
            
        doc_data = upload_resp.json()
        doc_id = doc_data['id']
        owner_id = doc_data.get('owner_id')
        print(f"Upload successful. Doc ID: {doc_id}")
        
        if owner_id:
             print(f"Document Owner ID: {owner_id}")
        else:
             print("WARNING: owner_id not returned in response.")

        # 4. Verify Document Details
        print(f"Verifying document details for ID: {doc_id}")
        # Note: Depending on my implementation, getting document might require auth or not.
        # usually get_document expects auth? Let's check router.
        # @router.get("/{document_id}", ...) -> current_user = Depends(get_current_user)
        # Yes it requires auth.
        
        get_resp = requests.get(f"{BASE_URL}/api/documents/{doc_id}", headers=headers)
        if get_resp.status_code != 200:
            print(f"Get Document failed: {get_resp.text}")
            return False
            
        get_data = get_resp.json()
        if get_data.get('owner_id') == owner_id:
            print("Verification Successful: Document linked to user correctly.")
            return True
        else:
            print(f"Verification Failed: Owner mismatch. Got {get_data.get('owner_id')}, expected {owner_id}")
            return False

    except Exception as e:
        print(f"Exception during verification: {e}")
        return False

if __name__ == "__main__":
    if run_verification():
        sys.exit(0)
    else:
        sys.exit(1)
