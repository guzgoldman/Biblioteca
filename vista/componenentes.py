# componenentes.py  (respeta tu nombre de archivo "componenentes.py")
import customtkinter as ctk
from PIL import Image
import os

def load_icons():
    icons_path = os.path.join(os.path.dirname(__file__), "icons")
    def icon(path, size=(20, 20)):
        full = os.path.join(icons_path, path)
        return ctk.CTkImage(light_image=Image.open(full), size=size) if os.path.exists(full) else None
    return {
        "home": icon("home.png"),
        "user": icon("user.png"),
        "book": icon("book.png"),
        "send": icon("send.png"),
        "logout": icon("logout.png"),
        "check": icon("check.png"),
        "cancel": icon("cancel.png"),
        "calendar": icon("calendar.png"),
    }

def default_menu(actions=None):
    items = [
        ("Escritorio", "home"),
        ("Socios", "user"),
        ("Libros", "book"),
        ("Préstamos", "send"),
        ("Salir", "logout"),
    ]
    if actions:
        return [(text, icon, actions.get(text)) for text, icon in items]
    return items

# componenentes.py — Sidebar (parche: coloca submenú justo debajo del botón padre)

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, icons, menu_items=None, actions=None, submenus=None, **kwargs):
        super().__init__(master, width=180, corner_radius=0, **kwargs)
        self.icons = icons
        self._submenu_frames = {}
        self._submenu_open = {}
        self._menu_buttons = {}       # 👈 NUEVO: guardamos el botón padre
        self.submenus = submenus or {}
        self.actions = actions or {}

        ctk.CTkLabel(self, text="Menú", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

        if menu_items:
            for item in menu_items:
                if len(item) == 2:
                    text, icon = item
                    command = self.actions.get(text)
                elif len(item) == 3:
                    text, icon, command = item
                else:
                    continue

                if text in self.submenus:
                    # Botón padre (Préstamos)
                    btn = ctk.CTkButton(
                        self, text=text, image=self.icons.get(icon), compound="left",
                        anchor="w", width=160, command=lambda t=text: self._toggle_submenu(t)
                    )
                    btn.pack(pady=5, padx=10)
                    self._menu_buttons[text] = btn  # 👈 guardar referencia del botón

                    # Frame del submenú (NO lo packeamos ahora)
                    frame = ctk.CTkFrame(self, fg_color="transparent")
                    self._submenu_frames[text] = frame
                    self._submenu_open[text] = False

                    # Hijos del submenú
                    for (child_text, child_cmd) in self.submenus[text]:
                        cbtn = ctk.CTkButton(
                            frame, text=f"• {child_text}", anchor="w", width=150, command=child_cmd
                        )
                        cbtn.pack(pady=3, padx=14)
                else:
                    btn = ctk.CTkButton(
                        self, text=text, image=self.icons.get(icon), compound="left",
                        anchor="w", width=160, command=command
                    )
                    btn.pack(pady=5, padx=10)

    def _toggle_submenu(self, key):
        frame = self._submenu_frames.get(key)
        parent_btn = self._menu_buttons.get(key)
        if not frame or not parent_btn:
            return

        open_now = not self._submenu_open.get(key, False)
        self._submenu_open[key] = open_now

        if open_now:
            # 👇 Empaca el submenú PEGADO al botón padre
            frame.pack(after=parent_btn, pady=(0, 6), padx=10, fill="x")
        else:
            frame.pack_forget()

class Banner(ctk.CTkLabel):
    def __init__(self, master, banner_path, **kwargs):
        banner_img = ctk.CTkImage(light_image=Image.open(banner_path), size=(master.winfo_width(), 150))
        super().__init__(
            master,
            text="Biblioteca Pública - Panel de Control",
            image=banner_img,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="black",
            compound="center",
            **kwargs
        )
        self.image = banner_img

class BaseWindow(ctk.CTk):
    """Ventana base con Sidebar + Banner reutilizable."""
    def __init__(self, title="Biblioteca", size="1000x600", banner_path="vista/images/banner_bandera.jpg"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.icons = load_icons()

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.sidebar = None

        self.main_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.banner_original = Image.open(banner_path)
        self.banner_label = Banner(self.main_frame, banner_path)
        self.banner_label.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        def update_banner(event=None):
            width = self.main_frame.winfo_width()
            banner_img = ctk.CTkImage(light_image=self.banner_original, size=(width, 150))
            self.banner_label.configure(image=banner_img)
            self.banner_label.image = banner_img

        self.main_frame.bind("<Configure>", update_banner)

    # Helper opcional para crear sidebar con acciones
    def build_sidebar(self, actions):
        self.sidebar = Sidebar(self.container, self.icons, default_menu(actions))
        self.sidebar.grid(row=0, column=0, sticky="ns")
        return self.sidebar
