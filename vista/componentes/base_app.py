import customtkinter as ctk
from db.Conector import Conector

class BaseApp(ctk.CTk):
    """Ventana base para todas las vistas: pantalla completa por defecto."""
    def __init__(self, title="Biblioteca Pública"):
        super().__init__()
        self.title(title)
        self.session = Conector.get_session()
        self.after(100, lambda: self._set_fullscreen())

    def _set_fullscreen(self):
        try:
            self.state("zoomed")  # Windows
        except Exception:
            self.attributes("-fullscreen", True)  # Linux/Mac