# loan_active_list.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from datetime import date
from sqlalchemy.orm import Session

from componenentes import BaseWindow, Sidebar, default_menu
from table_widget import Table
from db.Conector import SessionLocal
from modelo.Prestamo import Prestamo
# Relaciona a Socio, Ejemplar (codigo, numero), Libro (titulo) vía relationships:contentReference[oaicite:3]{index=3}:contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoanActiveList(BaseWindow):
    def __init__(self):
        super().__init__(title="Préstamos Activos")

        actions = {
            "Escritorio": self.go_dashboard,
            "Socios": self.go_socios,
            "Libros": self.go_books,
            "Préstamos": self.toggle_prestamos,
            "Salir": self.quit
        }
        # Submenú para Préstamos
        submenus = {
            "Préstamos": [
                ("Activos", self.go_prestamos_activos),
                ("Historial", self.go_prestamos_historial)
            ]
        }
        self.build_sidebar_with_submenus(actions, submenus)

        # Contenido
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)
        ctk.CTkLabel(self.content_frame, text="Préstamos activos", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        columns = [
            {"key": "dni", "text": "DNI", "width": 120},
            {"key": "nombre", "text": "Nombre", "width": 150},
            {"key": "apellido", "text": "Apellido", "width": 150},
            {"key": "titulo", "text": "Título", "width": 220},
            {"key": "isbn", "text": "ISBN", "width": 130},
            {"key": "ejemplar", "text": "Ejemplar", "width": 100},
            {"key": "fecha_solicitado", "text": "Fecha solicitado", "width": 140},
            {"key": "fecha_devolucion", "text": "Fecha devolución", "width": 140},
            {"key": "estado", "text": "Estado", "width": 120},
        ]
        self.table = Table(self.content_frame, columns, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        self.load_data()

    def build_sidebar_with_submenus(self, actions, submenus):
        # helper usando Sidebar mejorado (ver cambios en componenentes.py abajo)
        self.sidebar = None
        self.sidebar = Sidebar(self.container, self.icons, default_menu(actions), actions=actions, submenus=submenus)
        self.sidebar.grid(row=0, column=0, sticky="ns")

    def load_data(self):
        session: Session = SessionLocal()
        activos = session.query(Prestamo).filter(Prestamo.fecha_devolucion == None).all()
        rows = []
        today = date.today()

        def fmt(dttm):
            if not dttm:
                return ""
            d = dttm.date() if hasattr(dttm, "date") else dttm
            return f"{d.day:02d}/{d.month:02d}/{d.year:04d}"

        for p in activos:
            socio = p.socio
            ej = p.ejemplar
            libro = ej.libro if ej else None
            pactada = p.fecha_devolucion_pactada.date() if hasattr(p.fecha_devolucion_pactada, "date") else p.fecha_devolucion_pactada
            dias_rest = (pactada - today).days if pactada else 0

            # Color según regla:
            # ≥4 -> verde | 1..3 -> amarillo | hoy o pasado (<=0) -> rojo
            if dias_rest >= 4:
                estado_bg = "#27ae60"
            elif 1 <= dias_rest <= 3:
                estado_bg = "#f1c40f"
            else:
                estado_bg = "#e74c3c"

            rows.append({
                "dni": getattr(socio, "dni", ""),
                "nombre": getattr(socio, "nombre", ""),
                "apellido": getattr(socio, "apellido", ""),
                "titulo": getattr(libro, "titulo", ""),
                "isbn": getattr(ej, "codigo", ""),
                "ejemplar": getattr(ej, "numero_ejemplar", ""),
                "fecha_solicitado": fmt(p.fecha_prestamo),
                "fecha_devolucion": fmt(p.fecha_devolucion_pactada),
                "estado": "Activo",
                "estado_bg": estado_bg,
            })

        session.close()
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
        from books_list import BookList
        self.destroy()
        BookList().mainloop()

    def go_prestamos_activos(self):
        self.destroy()
        LoanActiveList().mainloop()

    def go_prestamos_historial(self):
        from loan_history_list import LoanHistoryList
        self.destroy()
        LoanHistoryList().mainloop()

    def toggle_prestamos(self):
        # El Sidebar maneja el despliegue; este método es sólo placeholder para 'Préstamos'
        pass

def main():
    app = LoanActiveList()
    app.mainloop()

if __name__ == "__main__":
    main()