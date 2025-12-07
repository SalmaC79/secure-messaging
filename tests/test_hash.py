import sys
import os

BASE_DIR = os.path.dirname(__file__)       # /project/tests
SRC_PATH = os.path.abspath(os.path.join(BASE_DIR, ".."))  # /project

sys.path.append(SRC_PATH)

from src.hash_module import hash_message, hash_file


try :
    # --- Test message as string ---
    msg_str = "hello world"
    hash_str = hash_message(msg_str)

    # --- Test message as bytes ---
    msg_bytes = b"hello world"
    hash_bytes = hash_message(msg_bytes)

    print("String input hash: ", hash_str)
    print("Bytes input hash:  ", hash_bytes)
    print("Hashes are identical? ->", hash_str == hash_bytes)
except Exception as e:
    print(e)

# --- Test file hashing ---
print("\nFile hashing test:")

test_file_path = os.path.join(BASE_DIR, "test.txt")
# test_file_path = "/home/nezha-halla/Downloads/CH1_BC.pdf" // test existing file in your system

# Create file in tests/
with open(test_file_path, "w") as f:
    f.write("this is a test file")

try :
    file_hash_1 = hash_file(test_file_path)
    print("File Hash 1:", file_hash_1)
except Exception as e:
    print(e)
