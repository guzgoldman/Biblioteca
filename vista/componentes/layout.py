import customtkinter as ctk
from .banner import Banner
from .sidebar import Sidebar
from .mainframe import MainFrame
from .utils import load_icons, default_menu

class AppLayout(ctk.CTkFrame):
    def __init__(self, master, banner_image=None, callbacks=None, admin=None, **kwargs):
        
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.session = getattr(master, "session", None)
        self.admin = admin
        self.icons = load_icons()
        self.menu_items = default_menu()

        self.sidebar = Sidebar(self, self.icons, self.menu_items, callbacks, self.admin)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.banner = Banner(self.main_frame, banner_image)
        self.banner.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    def clear_main_content(self):
        """Elimina todo el contenido del main frame excepto el banner."""
        for widget in self.main_frame.grid_slaves():
            if widget.grid_info().get("row") != 0:
                widget.destroy()