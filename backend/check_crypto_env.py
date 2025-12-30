import sys
try:
    import pymysql
    import cryptography
    from cryptography.hazmat.primitives import serialization
    print(f"PyMySQL Version: {pymysql.__version__}")
    print(f"Cryptography Version: {cryptography.__version__}")
    print("Successfully imported cryptography.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
