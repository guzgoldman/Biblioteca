import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from componentes import AppLayout, BaseApp, Table, get_default_callbacks
from db.Conector import SessionLocal
from modelo.Libro import Libro
from modelo.Ejemplar import Ejemplar

class BookList(BaseApp):
    def __init__(self):
        super().__init__(title="Biblioteca Pública - Socios")

        callbacks = get_default_callbacks(self)

        # Estructura base
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        # Configurar filas y columnas principales
        self.layout.main_frame.grid_rowconfigure(1, weight=1)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        # Frame del contenido
        self.content_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)

        # Título
        ctk.CTkLabel(
            self.content_frame,
            text="Listado de Socios",
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

        # Tabla reutilizable
        self.table = Table(self.content_frame, columns, width=900, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        # Cargar datos
        self.load_data()

    def load_data(self):
        session = SessionLocal()
        libros = session.query(Libro).all()
        print(libros)
        ejemplares = session.query(Ejemplar).all()
        print(ejemplares)
        session.close()

        libros_by_id = {l.id: l for l in libros}
        rows = []
        for e in ejemplares:
            lib = libros_by_id.get(e.libro_id)
            if not lib:
                continue
            rows.append({
                "titulo": getattr(lib, "titulo", ""),
                "autor": getattr(lib, "autor", ""),
                "isbn": getattr(lib, "isbn", ""),
                "ejemplar": getattr(e, "numero_ejemplar", ""),
                "estado": "Disponible" if getattr(e, "disponible", False) else "No disponible"
            })
        self.table.set_data(rows)

def main():
    app = BookList()
    app.mainloop()

if __name__ == "__main__":
    main()