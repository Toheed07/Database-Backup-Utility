from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()


key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)


def encrypt_file(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)

    encrypted_file_path = f"{file_path}.enc"
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)

    return encrypted_file_path


def decrypt_file(file_path):
    if not file_path.endswith(".enc"):
        raise ValueError("The file does not have the expected .enc extension.")

    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    data = cipher.decrypt(encrypted_data)

    original_file_path = file_path[:-4]
    with open(original_file_path, "wb") as file:
        file.write(data)

    return original_file_path
