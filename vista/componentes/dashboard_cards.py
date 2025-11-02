import customtkinter as ctk
import os
from PIL import Image


class DashboardCards(ctk.CTkFrame):
    """
    Componente reutilizable para mostrar cards en el dashboard.
    Permite hover animado y callback opcional.
    
    Ejemplo:
        cards_info = [
            {"titulo": "SOCIOS", "pie": "Alta usuario | Editar usuario", "color": "#3498DB", "icon": "people.png"},
            {"titulo": "LIBROS", "pie": "Cargar libro", "color": "#2ECC71", "icon": "book.png"},
        ]
        cards = DashboardCards(master, cards_info=cards_info)
    """
    def __init__(self, master, cards_info: list[dict], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.cards_info = cards_info

        self.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        self.grid_rowconfigure((0, 1), weight=1, uniform="rows")

        for idx, info in enumerate(self.cards_info):
            fila, col = divmod(idx, 2)
            card = self._create_card(info)
            card.grid(row=fila, column=col, padx=20, pady=20, sticky="nsew")

    # ======================================================
    def _create_card(self, info: dict):
        """Crea una card individual con hover y pie opcional."""
        color = info.get("color", "#3498DB")
        titulo = info.get("titulo", "")
        pie = info.get("pie", "")
        icon_name = info.get("icon", "")

        card = ctk.CTkFrame(self, fg_color=color, corner_radius=15)
        card.grid_propagate(False)
        card.configure(width=350, height=180)

        # ================== Hover animado ==================
        def on_enter(e):
            card.configure(fg_color=self._darken_color(color, 0.15))

        def on_leave(e):
            card.configure(fg_color=color)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        # ===================================================

        # Icono y título
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(pady=(25, 10))

        icon_path = os.path.join("vista", "icons", icon_name)
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((40, 40))
            icon_img = ctk.CTkImage(light_image=img, size=(40, 40))
            lbl_icon = ctk.CTkLabel(header, image=icon_img, text="")
            lbl_icon.image = icon_img
            lbl_icon.pack(side="left", padx=(0, 10))

        lbl_titulo = ctk.CTkLabel(header, text=titulo, text_color="white",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.pack(side="left")
        card.titulo = titulo

        # Placeholder para valor dinámico (se rellena desde el Dashboard)
        value_label = ctk.CTkLabel(card, text="--", text_color="white",
                                   font=ctk.CTkFont(size=48, weight="bold"))
        value_label.pack(pady=(10, 0))
        card.value_label = value_label
        
        separator = ctk.CTkFrame(card, height=2, fg_color="white")
        separator.pack(fill="x", padx=60, pady=(0, 8))  # más cerca del footer
        card.separator = separator
        
        pie = info.get("pie", "")
        pie_formatted = "   |   ".join(p.strip() for p in pie.split("|")) if "|" in pie else pie
        # Footer de texto (sin eventos, se maneja desde main_dashboard)
        footer = ctk.CTkLabel(card, text=pie, text_color="white",
                              font=ctk.CTkFont(size=14, weight="bold"))
        footer.pack(side="bottom", pady=10)
        card.footer_label = footer

        return card

    # ======================================================
    def _darken_color(self, hex_color, factor=0.2):
        """Oscurece un color hexadecimal."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (1 - factor))) for c in rgb)
        return f"#{darkened[0]:02X}{darkened[1]:02X}{darkened[2]:02X}"

    # ======================================================
    def get_card_by_title(self, title: str):
        """Devuelve la card según su título (para actualizar valores)."""
        for card in self.winfo_children():
            if getattr(card, "titulo", "").strip().lower() == title.strip().lower():
                return card
        return None
