import os
import customtkinter as ctk
from PIL import Image

def load_icons():
    """Carga los íconos desde la carpeta vistas/icons con rutas absolutas."""
    # 🔥 ruta absoluta (independiente del directorio actual)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))

    def icon(filename, size=(22, 22)):
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            try:
                return ctk.CTkImage(light_image=Image.open(path), size=size)
            except Exception as e:
                print(f"[WARN] No se pudo cargar ícono '{filename}': {e}")
                return None
        else:
            print(f"[WARN] Ícono no encontrado: {path}")
            return None

    return {
        "home": icon("home.png"),
        "user": icon("user.png"),
        "book": icon("book.png"),
        "send": icon("librarian.png"),
        "logout": icon("logout.png"),
        "calendar": icon("calendar.png"),
        "main_user": icon("main_user.png", size=(70, 70)),
    }



def default_menu():
    """Define la estructura del menú lateral."""
    return [
        ("Escritorio", "home"),
        ("Socios", "user"),
        ("Libros", "book"),
        ("Préstamos", "send"),
        ("Salir", "logout"),
    ]