import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from datetime import date

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.table import Table
from vista.componentes.callbacks import get_default_callbacks

from modelo.Prestamo import Prestamo
from modelo.Ejemplar import Ejemplar
from modelo.Libro import Libro
from modelo.Socio import Socio

from sqlalchemy.orm import joinedload
from db.session_manager import SessionManager


class LoanHistoryList(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Biblioteca Pública - Historial de Préstamos")

        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)

        # Estructura base
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self.layout.main_frame.grid_rowconfigure(1, weight=1)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        # Contenedor principal
        self.content_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)

        ctk.CTkLabel(
            self.content_frame,
            text="Historial de Préstamos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Definición de columnas
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

        self.table = Table(self.content_frame, columns, width=900, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        self.load_data()

    # ===========================================================
    def load_data(self):
        """Carga el historial de préstamos usando la sesión compartida."""
        if not self.session:
            raise ValueError("No se recibió una sesión de base de datos válida.")

        # Traer préstamos devueltos junto con socio, ejemplar y libro
        devueltos = (
            self.session.query(Prestamo)
            .options(
                joinedload(Prestamo.socio),
                joinedload(Prestamo.ejemplar).joinedload(Ejemplar.libro)
            )
            .filter(Prestamo.fecha_devolucion.isnot(None))
            .all()
        )

        rows = []
        for p in devueltos:
            socio = p.socio
            ej = p.ejemplar
            libro = ej.libro if ej else None

            pactada = getattr(p, "fecha_devolucion_pactada", None)
            dev = getattr(p, "fecha_devolucion", None)
            pactada = pactada.date() if hasattr(pactada, "date") else pactada
            dev = dev.date() if hasattr(dev, "date") else dev

            on_time = (dev and pactada and dev <= pactada)
            estado_bg = "#27ae60" if on_time else "#e74c3c"

            rows.append({
                "dni": getattr(socio, "dni", ""),
                "nombre": getattr(socio, "nombre", ""),
                "apellido": getattr(socio, "apellido", ""),
                "titulo": getattr(libro, "titulo", ""),
                "isbn": getattr(libro, "isbn", ""),
                "ejemplar": getattr(ej, "numero_ejemplar", ""),
                "fecha_solicitado": self.formato_fecha(p.fecha_prestamo),
                "fecha_devolucion": self.formato_fecha(p.fecha_devolucion),
                "estado": "Devuelto",
                "estado_bg": estado_bg,
            })

        self.table.set_data(rows)

    # ===========================================================
    def formato_fecha(self, dttm):
        if not dttm:
            return ""
        d = dttm.date() if hasattr(dttm, "date") else dttm
        return f"{d.day:02d}/{d.month:02d}/{d.year:04d}"


if __name__ == "__main__":
    # Solo para pruebas: crea sesión temporal si no se pasa ninguna
    from db.Conector import SessionLocal
    app = LoanHistoryList(session=SessionLocal())
    app.mainloop()
