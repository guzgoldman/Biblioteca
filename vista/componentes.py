import customtkinter as ctk
from PIL import Image
from datetime import datetime
import os
import tkinter.ttk as ttk
from dashboard_stats import DashboardStats

class BaseApp(ctk.CTk):
    """Ventana base para todas las vistas: pantalla completa por defecto."""
    def __init__(self, title="Biblioteca Pública"):
        super().__init__()
        self.title(title)
        self.after(100, lambda: self._set_fullscreen())

    def _set_fullscreen(self):
        try:
            # En Windows
            self.state("zoomed")
        except Exception:
            # En Linux/Mac
            self.attributes("-fullscreen", True)


# ==========================================================
#   UTILIDADES DE ICONOS Y MENÚ
# ==========================================================
def load_icons():
    """Carga los íconos desde la carpeta vistas/icons"""
    icons_path = os.path.join(os.path.dirname(__file__), "icons")

    def icon(path, size=(20, 20)):
        full = os.path.join(icons_path, path)
        return ctk.CTkImage(light_image=Image.open(full), size=size) if os.path.exists(full) else None

    return {
        "home": icon("home.png"),
        "user": icon("user.png"),
        "book": icon("book.png"),
        "send": icon("librarian.png"),
        "logout": icon("logout.png"),
        "calendar": icon("calendar.png"),
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


# ==========================================================
#   COMPONENTES REUTILIZABLES
# ==========================================================
class Banner(ctk.CTkFrame):
    """
    Banner superior con imagen redimensionable (sin bucles infinitos ni retrasos).
    Dibuja instantáneamente al inicio y reajusta solo cuando cambia el ancho del contenedor.
    """
    def __init__(self, master, image_path=None, fixed_height=250, **kwargs):
        super().__init__(master, fg_color="white", height=fixed_height, corner_radius=0, **kwargs)
        self.grid_propagate(False)
        self.fixed_height = fixed_height

        self.label = ctk.CTkLabel(self, text="", fg_color="white")
        self.label.pack(fill="both", expand=True)

        self._banner_img_original = None
        self._last_width = 0
        self._image_path = image_path

        if image_path and os.path.exists(image_path):
            from PIL import Image
            self._banner_img_original = Image.open(image_path).convert("RGB")

        # Dibujar apenas el widget tenga tamaño válido
        self.after(100, self._initial_draw)

    def _initial_draw(self):
        """Dibuja el banner al inicio y vincula el evento de resize del contenedor."""
        if not self._banner_img_original:
            self.configure(fg_color="#2C3E50")
            return

        if self.winfo_width() < 50:
            # Aún no tiene tamaño real → reintentar
            self.after(100, self._initial_draw)
            return

        self._redraw_banner()
        # Vincular solo una vez: el resize del padre, no del banner
        if self.master:
            self.master.bind("<Configure>", self._on_parent_resize, add="+")

    def _on_parent_resize(self, event=None):
        """Redibuja solo si cambió significativamente el ancho del contenedor."""
        new_width = self.winfo_width()
        if abs(new_width - self._last_width) > 10:
            self._redraw_banner()

    def _redraw_banner(self):
        """Escala la imagen al ancho actual manteniendo altura fija."""
        if not self._banner_img_original:
            return

        width = max(50, self.winfo_width())
        height = self.fixed_height
        from PIL import ImageOps
        img = ImageOps.fit(self._banner_img_original, (width, height))
        tkimg = ctk.CTkImage(light_image=img, size=(width, height))
        self.label.configure(image=tkimg)
        self.label.image = tkimg
        self._last_width = width

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, icons, menu_items, callbacks=None, **kwargs):
        super().__init__(master, fg_color="#2C3E50", width=220, corner_radius=0, **kwargs)
        self.grid_propagate(False)

        self.icons = icons
        self.callbacks = callbacks or {}

        # Cabecera
        header = ctk.CTkLabel(self, text="Biblioteca Pública",
                              font=ctk.CTkFont(size=22, weight="bold"),
                              text_color="white")
        header.pack(pady=(20, 10))

        # Icono de usuario
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "main_user.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((70, 70))
            user_img = ctk.CTkImage(light_image=img, size=(70, 70))
            lbl_icon = ctk.CTkLabel(self, image=user_img, text="")
            lbl_icon.image = user_img
            lbl_icon.pack(pady=(0, 10))

        # Nombre usuario + fecha
        lbl_user = ctk.CTkLabel(self, text="Admin",
                                font=ctk.CTkFont(size=18, weight="bold"),
                                text_color="white")
        lbl_user.pack()

        lbl_date = ctk.CTkLabel(self,
                                text=f"Logueado: {DashboardStats.obtener_fecha_actual()}",
                                font=ctk.CTkFont(size=14),
                                text_color="#D5D8DC")
        lbl_date.pack(pady=(0, 15))

        # Separador
        sep = ctk.CTkFrame(self, height=2, fg_color="#BDC3C7")
        sep.pack(fill="x", padx=10, pady=(10, 10))

        # Botones del menú
        for text, icon in menu_items:
            cmd = self.callbacks.get(text, None)
            btn = ctk.CTkButton(self,
                                text=text,
                                image=self.icons.get(icon),
                                compound="left",
                                anchor="w",
                                fg_color="#2E86C1",
                                hover_color="#1B4F72",
                                corner_radius=8,
                                height=40,
                                command=cmd)
            btn.pack(fill="x", padx=15, pady=5)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=0, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

# ==========================================================
#   LAYOUT BASE DE LA APLICACIÓN
# ==========================================================

class AppLayout(ctk.CTkFrame):
    def __init__(self, master, banner_image=None, callbacks=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Carga de íconos y menú
        self.icons = load_icons()
        self.menu_items = default_menu()

        # Sidebar
        self.sidebar = Sidebar(self, self.icons, self.menu_items, callbacks)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main frame
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Banner dentro del main_frame
        print(banner_image)
        self.banner = Banner(self.main_frame, banner_image)
        self.banner.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    def clear_main_content(self):
        """Elimina el contenido del main frame (excepto el banner)."""
        for widget in self.main_frame.grid_slaves():
            info = widget.grid_info()
            if info.get("row") != 0:  # deja el banner
                widget.destroy()

# ==========================================================
#   CALLBACKS COMUNES PARA TODAS LAS VISTAS
# ==========================================================
def get_default_callbacks(app):
    """Devuelve el diccionario de callbacks comunes para todas las vistas."""
    from componentes import go_to_dashboard, go_to_users, go_to_books, go_to_loans, go_to_exit

    return {
        "Escritorio": lambda: go_to_dashboard(app),
        "Socios": lambda: go_to_users(app),
        "Libros": lambda: go_to_books(app),
        "Préstamos": lambda: go_to_loans(app),
        "Salir": lambda: go_to_exit(app),
    }


# ==========================================================
#   TABLA
# ==========================================================

class Table(ctk.CTkFrame):
    """
    Tabla reutilizable con columnas configurables.
    columns = [
        {"key": "dni", "text": "DNI", "width": 120},
        {"key": "nombre", "text": "Nombre", "width": 180},
        ...
    ]
    """
    def __init__(self, master, columns, width=800, height=400, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=10, **kwargs)
        self.grid_propagate(False)
        self.configure(width=width, height=height)

        # Treeview base
        self.tree = ttk.Treeview(self, columns=[c["key"] for c in columns], show="headings", selectmode="browse")
        self.tree.pack(fill="both", expand=True, side="left")

        # Scrollbars
        y_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=y_scroll.set)

        # Configuración de columnas
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", rowheight=26, font=("Arial", 11))

        for col in columns:
            key, text, w = col["key"], col["text"], col.get("width", 100)
            self.tree.heading(key, text=text)
            self.tree.column(key, width=w, anchor="w")

    def set_data(self, data):
        """Carga los datos en la tabla, data es una lista de diccionarios."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            values = [row.get(col) for col in self.tree["columns"]]
            self.tree.insert("", "end", values=values)


# ==========================================================
#   MÉTODOS DE NAVEGACIÓN (PLACEHOLDERS)
# ==========================================================
def go_to_dashboard(current_window=None):
    from main_dashboard import MainDashboard
    if current_window:
        current_window.destroy()
    MainDashboard().mainloop()

def go_to_users(current_window=None):
    from users_list import UserList
    if current_window:
        current_window.destroy()
    UserList().mainloop()

def go_to_books(current_window=None):
    from books_list import BookList
    if current_window:
        current_window.destroy()
    BookList().mainloop()

def go_to_loans(current_window=None):
    from loan_history_list import LoanHistoryList
    if current_window:
        current_window.destroy()
    LoanHistoryList().mainloop()

def go_to_exit(current_window=None):
    if current_window:
        current_window.destroy()
