from cryptography.fernet import Fernet
import os

# Nombre del archivo donde se guardará la clave
KEY_FILE = "key.key"

# Evitar sobrescribir una clave existente
if os.path.exists(KEY_FILE):
    print(f"La clave ya existe: {KEY_FILE}")
else:
    # Generar una clave Fernet
    key = Fernet.generate_key()

    # Guardarla en un archivo binario
    with open(KEY_FILE, "wb") as file:
        file.write(key)

    print(f"Clave creada correctamente en '{KEY_FILE}'")
    print(f"Clave: {key.decode()}")