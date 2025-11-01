import customtkinter as ctk
from PIL import Image
import os
from vista.componentes.dashboard_stats import DashboardStats

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, icons, menu_items, callbacks=None, admin=None, **kwargs):
        super().__init__(master, fg_color="#2C3E50", width=220, corner_radius=0, **kwargs)
        self.grid_propagate(False)
        self.icons = icons
        self.admin = admin
        self.callbacks = callbacks or {}

        header = ctk.CTkLabel(self, text="Biblioteca Pública",
                              font=ctk.CTkFont(size=22, weight="bold"),
                              text_color="white")
        header.pack(pady=(20, 10))

        # Imagen usuario
        icon_path = os.path.join(os.path.dirname(__file__), "../icons/main_user.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((70, 70))
            user_img = ctk.CTkImage(light_image=img, size=(70, 70))
            lbl_icon = ctk.CTkLabel(self, image=user_img, text="")
            lbl_icon.image = user_img
            lbl_icon.pack(pady=(0, 10))
            
        admin_nombre = f"{self.admin.nombre} {self.admin.apellido}" if self.admin else "Admin"
        lbl_user = ctk.CTkLabel(self, text=admin_nombre,
                                font=ctk.CTkFont(size=18, weight="bold"),
                                text_color="white")
        lbl_user.pack()

        lbl_date = ctk.CTkLabel(self,
                                text=f"Logueado: {DashboardStats.obtener_fecha_actual()}",
                                font=ctk.CTkFont(size=14),
                                text_color="#D5D8DC")
        lbl_date.pack(pady=(0, 15))

        sep = ctk.CTkFrame(self, height=2, fg_color="#BDC3C7")
        sep.pack(fill="x", padx=10, pady=(10, 10))

        for text, icon in menu_items:
            cmd = self.callbacks.get(text, None)
            btn = ctk.CTkButton(self, text=text, image=self.icons.get(icon),
                                compound="left", anchor="w",
                                fg_color="#2E86C1", hover_color="#1B4F72",
                                corner_radius=8, height=40, command=cmd)
            btn.pack(fill="x", padx=15, pady=5)