import hashlib
import os

MAX_FILE_SIZE = 20 * 1024 * 1024

def hash_message(message: str, algorithm='sha256'):
    if isinstance(message, bytes):
        message = message.decode("utf-8", errors="replace")
    try:
        h = hashlib.new(algorithm)
        h.update(message.encode('utf-8'))
        return h.hexdigest()

    except ValueError:
        print(f"[ERROR] Unknown hashing algorithm: {algorithm}")
        return None

    except Exception as e:
        print(f"[ERROR] Message hashing failed: {e}")
        return None


def hash_file(file_path: str, algorithm='sha256', chunk_size=4096):
    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return None
    
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large to hash ({file_size} bytes). "
            f"Maximum allowed is {MAX_FILE_SIZE} bytes."
        )

    try:
        
        h = hashlib.new(algorithm)
    except ValueError:
        print(f"[ERROR] Unknown hashing algorithm: {algorithm}")
        return None

    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)

        return h.hexdigest()

    except PermissionError:
        print(f"[ERROR] Permission denied: unable to read the file '{file_path}'.")
        return None

    except Exception as e:
        print(f"[ERROR] File hashing failed: {e}")
        return None
