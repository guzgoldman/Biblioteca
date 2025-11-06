import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
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

def show_message(title, message, icon="info"):
    import tkinter as tk
    root = tk._default_root
    if root:
        root.lift()
        root.focus_force()
    msg = CTkMessagebox(title=title, message=message, icon=icon)
    msg.lift()
    msg.focus_force()
    return msg

def safe_messagebox(title="Mensaje", message="", level="info", buttons="ok", parent=None):
    """
    Dialogs nativos, sin imágenes. Devuelve:
      - "OK" para botones="ok"
      - "Aceptar"/"Cancelar" para botones="okcancel"
      - "Sí"/"No" para botones="yesno"
    level: "info" | "warning" | "error"
    """
    temp_root = None
    root = parent or tk._default_root
    if root is None or not isinstance(root, tk.Tk):
        temp_root = tk.Tk()
        temp_root.withdraw()
        root = temp_root

    try:
        if buttons == "ok":
            if level == "warning":
                messagebox.showwarning(title, message, parent=root)
            elif level == "error":
                messagebox.showerror(title, message, parent=root)
            else:
                messagebox.showinfo(title, message, parent=root)
            return "OK"

        if buttons == "okcancel":
            # askokcancel no tiene "info/warning/error" visibles, pero es estable.
            res = messagebox.askokcancel(title, message, parent=root, icon=level if level in ("warning","error") else "info")
            return "Aceptar" if res else "Cancelar"

        if buttons == "yesno":
            res = messagebox.askyesno(title, message, parent=root, icon=level if level in ("warning","error") else "info")
            return "Sí" if res else "No"

        # fallback
        messagebox.showinfo(title, message, parent=root)
        return "OK"
    finally:
        if temp_root:
            temp_root.destroy()
