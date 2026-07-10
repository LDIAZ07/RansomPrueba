from cryptography.fernet import Fernet
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEY_FILE = os.path.join(BASE_DIR, "key.key")

TARGET_FOLDER = os.path.expanduser("~")
# TARGET_FOLDER = "/home/vboxuser/Documents/archivos_importantes"

home = os.path.expanduser("~")

folders = [
    "Desktop",
    "Documents",
    "Downloads",
    "Music",
    "Pictures",
    "Public",
    "Templates",
    "Videos"
]


def load_key():
    """Carga la clave desde key.key"""
    with open(KEY_FILE, "rb") as file:
        return file.read()


def decrypt_file(file_path, cipher):
    """Descifra un archivo individual"""

    # Leer contenido cifrado
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    try:
        # Descifrar contenido
        decrypted_data = cipher.decrypt(encrypted_data)

        # Quitar extensión .encrypted
        original_path = file_path.replace(".encrypted", "")

        # Restaurar archivo original
        with open(original_path, "wb") as file:
            file.write(decrypted_data)

        # Eliminar archivo cifrado
        os.remove(file_path)

        print(f"Descifrado: {original_path}")

    except Exception:
        print(f"No se pudo descifrar: {file_path}")


def decrypt_folder(folders, cipher):

    for folder in folders:

        folder_path = os.path.join(home, folder)

        for root, directories, files in os.walk(folder_path):

            for file in files:

                file_path = os.path.join(root, file)

                # Solo descifrar archivos .encrypted
                if file.endswith(".encrypted"):
                    decrypt_file(file_path, cipher)


if __name__ == "__main__":

    # Validar existencia de clave
    if not os.path.exists(KEY_FILE):
        print("No existe key.key.")
        exit()

    # Validar carpeta
    if not os.path.exists(TARGET_FOLDER):
        print("La carpeta indicada no existe.")
        exit()


    key = load_key()

    cipher = Fernet(key)

    decrypt_folder(TARGET_FOLDER, cipher)

    print("\nProceso terminado.")
