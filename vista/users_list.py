import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import customtkinter as ctk
from datetime import date
from db.session_manager import SessionManager

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.table import Table
from vista.componentes.callbacks import get_default_callbacks

from modelo.Socio import Socio
from modelo.Prestamo import Prestamo


class UserList(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Biblioteca Pública - Socios")

        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)

        # Layout base
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self.layout.main_frame.grid_rowconfigure(1, weight=1)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        # Contenedor del contenido
        self.content_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=10)

        ctk.CTkLabel(
            self.content_frame,
            text="Listado de Socios",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Definición de columnas
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

    # =======================================================
    def load_data(self):
        """Carga la lista de socios y su estado de préstamo actual usando la sesión compartida."""
        if not self.session:
            raise ValueError("No se recibió una sesión de base de datos válida.")

        socios = self.session.query(Socio).all()
        prestamos_activos = (
            self.session.query(Prestamo)
            .filter(Prestamo.fecha_devolucion.is_(None))
            .all()
        )

        # Crear mapa de socios con préstamos activos
        activos_map = {}
        for p in prestamos_activos:
            pactada = getattr(p, "fecha_devolucion_pactada", None)
            if pactada and hasattr(pactada, "date"):
                pactada = pactada.date()
            estado = "Vencido" if (pactada and date.today() > pactada) else "Activo"
            activos_map[p.socio_id] = estado

        # Construir las filas para la tabla
        rows = []
        for s in socios:
            rows.append({
                "dni": s.dni,
                "nombre": s.nombre,
                "apellido": s.apellido,
                "direccion": getattr(s, "direccion", ""),
                "estado": activos_map.get(s.dni, "Inactivo"),
            })

        self.table.set_data(rows)


if __name__ == "__main__":
    # Solo para pruebas: crea una sesión temporal si no se pasa ninguna
    from db.Conector import SessionLocal
    app = UserList(session=SessionLocal())
    app.mainloop()