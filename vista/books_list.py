import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from db.session_manager import SessionManager

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.table import Table
from vista.componentes.callbacks import get_default_callbacks

from modelo.Libro import Libro
from modelo.Ejemplar import Ejemplar


class BookList(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Biblioteca Pública - Libros")
        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)

        # Layout base
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self.layout.main_frame.grid_rowconfigure(1, weight=1)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        # Contenedor principal
        self.content_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)

        ctk.CTkLabel(
            self.content_frame,
            text="Listado de Libros",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Definir columnas
        columns = [
            {"key": "titulo", "text": "Título", "width": 220},
            {"key": "autor", "text": "Autor", "width": 200},
            {"key": "isbn", "text": "ISBN", "width": 140},
            {"key": "ejemplar", "text": "Ejemplar", "width": 100},
            {"key": "estado", "text": "Estado", "width": 120},
        ]

        self.table = Table(self.content_frame, columns, width=900, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        self.load_data()

    # =======================================================
    def load_data(self):
        """Carga libros y ejemplares desde la sesión compartida."""
        if not self.session:
            raise ValueError("No se recibió una sesión de base de datos válida.")

        libros = self.session.query(Libro).all()
        ejemplares = self.session.query(Ejemplar).all()

        # Crear mapa ISBN → Libro
        libros_by_isbn = {l.isbn: l for l in libros}
        rows = []

        for e in ejemplares:
            lib = libros_by_isbn.get(e.libro_isbn)
            if not lib:
                continue
            rows.append({
                "titulo": lib.titulo,
                "autor": lib.autor,
                "isbn": lib.isbn,
                "ejemplar": e.numero_ejemplar,
                "estado": "Disponible" if e.disponible else "No disponible"
            })

        self.table.set_data(rows)

if __name__ == "__main__":
    app = BookList()
    app.mainloop()