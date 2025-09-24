# users_list.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from sqlalchemy.orm import Session
from datetime import date
from componenentes import BaseWindow
from table_widget import Table
from db.Conector import SessionLocal
from modelo.Socio import Socio
from modelo.Prestamo import Prestamo

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class UserList(BaseWindow):
    def __init__(self):
        super().__init__(title="Listado de Socios")

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

        ctk.CTkLabel(self.content_frame, text="Listado de Socios", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Tabla
        columns = [
            {"key": "dni", "text": "DNI", "width": 120},
            {"key": "nombre", "text": "Nombre", "width": 180},
            {"key": "apellido", "text": "Apellido", "width": 180},
            {"key": "direccion", "text": "Dirección", "width": 240},
            {"key": "estado", "text": "Estado Préstamo", "width": 150},
        ]
        self.table = Table(self.content_frame, columns, width=900, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        self.load_data()

    def load_data(self):
        session: Session = SessionLocal()
        socios = session.query(Socio).all()
        prestamos_activos = session.query(Prestamo).filter(Prestamo.fecha_devolucion == None).all()
        session.close()

        activos_map = {}
        for p in prestamos_activos:
            pactada = p.fecha_devolucion_pactada
            pactada = pactada.date() if hasattr(pactada, "date") else pactada
            estado = "Vencido" if (pactada and date.today() > pactada) else "Activo"
            activos_map[p.socio_id] = estado

        rows = []
        for s in socios:
            rows.append({
                "dni": s.dni,
                "nombre": s.nombre,
                "apellido": s.apellido,
                "direccion": getattr(s, "direccion", ""),
                "estado": activos_map.get(s.id, "Inactivo")
            })
        self.table.set_data(rows)

    # Navegación (cierra ventana actual y abre la siguiente)
    def go_dashboard(self):
        from main_dashboard import mainDashBoard
        self.destroy()
        mainDashBoard().mainloop()

    def go_socios(self):
        self.destroy()
        UserList().mainloop()

    def go_books(self):
        from books_list import BookList
        self.destroy()
        BookList().mainloop()

    def go_prestamos(self):
        # Pendiente: implementar vista de préstamos
        pass

def main():
    app = UserList()
    app.mainloop()

if __name__ == "__main__":
    main()
