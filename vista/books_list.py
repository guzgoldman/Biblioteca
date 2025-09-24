# books_list.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from sqlalchemy.orm import Session
from componenentes import BaseWindow
from table_widget import Table
from db.Conector import SessionLocal
from modelo.Libro import Libro
from modelo.Ejemplar import Ejemplar

class BookList(BaseWindow):
    def __init__(self):
        super().__init__(title="Listado de Libros")

        actions = {
            "Escritorio": self.go_dashboard,
            "Socios": self.go_socios,
            "Libros": self.go_books,
            "Préstamos": self.go_prestamos,
            "Salir": self.quit
        }
        self.build_sidebar(actions)

        # Contenedor
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)

        ctk.CTkLabel(self.content_frame, text="Listado de Libros y Ejemplares", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        columns = [
            {"key": "titulo", "text": "Título", "width": 220},
            {"key": "autor", "text": "Autor", "width": 200},
            {"key": "isbn", "text": "ISBN", "width": 140},
            {"key": "ejemplar", "text": "Ejemplar", "width": 100},
            {"key": "estado", "text": "Estado", "width": 120},
        ]
        self.table = Table(self.content_frame, columns, width=920, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        self.load_data()

    def load_data(self):
        session: Session = SessionLocal()
        libros = session.query(Libro).all()
        ejemplares = session.query(Ejemplar).all()
        session.close()

        # Indexar libros por id
        libros_by_id = {l.id: l for l in libros}
        rows = []
        for e in ejemplares:
            lib = libros_by_id.get(e.libro_id)
            if not lib:
                continue
            rows.append({
                "titulo": getattr(lib, "titulo", ""),
                "autor": getattr(lib, "autor", ""),
                "isbn": getattr(e, "codigo", ""),
                "ejemplar": getattr(e, "numero_ejemplar", ""),
                "estado": "Disponible" if getattr(e, "disponible", False) else "No disponible"
            })
        self.table.set_data(rows)

    # Navegación
    def go_dashboard(self):
        from main_dashboard import mainDashBoard
        self.destroy()
        mainDashBoard().mainloop()

    def go_socios(self):
        from users_list import UserList
        self.destroy()
        UserList().mainloop()

    def go_books(self):
        self.destroy()
        BookList().mainloop()

    def go_prestamos(self):
        # Pendiente: implementar vista de préstamos
        pass

def main():
    app = BookList()
    app.mainloop()

if __name__ == "__main__":
    main()
