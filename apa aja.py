import os
from cryptography.fernet import Fernet
from pathlib import Path
import getpass

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(file_path):
    key = load_key()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    print(f"File terenkripsi: {file_path}")

def decrypt_file(file_path):
    key = load_key()
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    print(f"File terdekripsi: {file_path}")

def encrypt_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path)

def decrypt_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            decrypt_file(file_path)

def verify_key():
    input_key = getpass.getpass("Masukkan kunci untuk membuka kunci folder: ")
    try:
        key = load_key()
        if input_key.encode() == key:  
            return True
        else:
            print("Kunci salah!")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    folder_target = str(Path.home() / "Downloads")

    if not os.path.exists("secret.key"):
        generate_key()
        print("Kunci enkripsi telah dibuat.")
    
    action = input("Ketik 'lock' untuk mengenkripsi atau 'unlock' untuk mendekripsi folder: ").strip().lower()
    
    if action == 'lock':
        encrypt_folder(folder_target)
        print("Semua file dalam folder telah terenkripsi.")
    elif action == 'unlock':
        if verify_key():
            decrypt_folder(folder_target)
            print("Semua file dalam folder telah didekripsi.")
        else:
            print("Gagal mendekripsi folder. Kunci salah.")
    else:
        print("Perintah tidak dikenali.")
