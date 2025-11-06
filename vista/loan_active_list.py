import os
import customtkinter as ctk
from datetime import date, datetime
from sqlalchemy.orm import joinedload

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from vista.componentes.table import Table  # tu Table modular
from vista.componentes.utils import safe_messagebox

from db.session_manager import SessionManager
from modelo.Prestamo import Prestamo
from modelo.Ejemplar import Ejemplar


class LoanActiveList(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Biblioteca Pública - Préstamos Activos")
        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)
        banner_path = os.path.join("vista", "images", "banner_bandera.jpg")

        self.layout = AppLayout(self, banner_image=banner_path, callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self.layout.main_frame.grid_rowconfigure(1, weight=1)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        title = ctk.CTkLabel(self.content_frame, text="📋 Préstamos Activos",
                             font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Orden y nombres de columnas EXACTOS con los datos
        self.columns = [
            {"key": "dni",               "text": "DNI",             "width": 110},
            {"key": "nombre",            "text": "Nombre",          "width": 140},
            {"key": "apellido",          "text": "Apellido",        "width": 140},
            {"key": "titulo",            "text": "Título",          "width": 230},
            {"key": "codigo",            "text": "Código ejemplar", "width": 140},
            {"key": "numero",            "text": "N° Ejemplar",     "width": 95},
            {"key": "fecha_prestamo",    "text": "Fecha préstamo",  "width": 135},
            {"key": "fecha_pactada",     "text": "Fecha devolución", "width": 150},  # se colorea
            {"key": "accion",            "text": "",                "width": 110},   # texto 'Cerrar'
        ]

        self.table = Table(self.content_frame, self.columns, width=1100, height=460)
        self.table.grid(row=1, column=0, sticky="nsew")

        # Configura tags de color
        if hasattr(self.table, "tag_config"):
            self.table.tag_config()

        # Bind click en celdas (para la columna 'accion')
        self.table.bind_cell_click(self._on_cell_click)

        self._rows_index = {}  # row_id -> prestamo_id
        self.load_data()

    # ------------------------------------------------------
    # Data
    def load_data(self):
        session = self.session
        today = date.today()
        self._rows_index.clear()

        activos = (
            session.query(Prestamo)
            .options(
                joinedload(Prestamo.socio),
                joinedload(Prestamo.ejemplar).joinedload(Ejemplar.libro),
            )
            .filter(Prestamo.fecha_devolucion.is_(None))
            .order_by(Prestamo.fecha_prestamo.desc())
            .all()
        )

        # Limpia la tabla
        for item in self.table.tree.get_children():
            self.table.tree.delete(item)

        for p in activos:
            socio = p.socio
            ej = p.ejemplar
            libro = ej.libro if ej else None

            pactada_d = p.fecha_devolucion_pactada.date() if p.fecha_devolucion_pactada else None
            # Tag de color para pactada
            tag = "due_green"
            if pactada_d is None or pactada_d <= today:
                tag = "due_red"

            values = {
                "dni": getattr(socio, "dni", ""),
                "nombre": getattr(socio, "nombre", ""),
                "apellido": getattr(socio, "apellido", ""),
                "titulo": getattr(libro, "titulo", "") if libro else "",
                "codigo": getattr(ej, "codigo", ""),
                "numero": getattr(ej, "numero_ejemplar", ""),
                "fecha_prestamo": self._fmt_fecha(p.fecha_prestamo),
                "fecha_pactada": self._fmt_fecha(p.fecha_devolucion_pactada),
                "accion": "Cerrar",
            }

            row_id = self.table.tree.insert("", "end",
                                            values=[values[c["key"]] for c in self.columns],
                                            tags=(tag,))
            self._rows_index[row_id] = p.id  # mapear fila -> id de préstamo

        # Para que la columna 'accion' no se estire
        self.table.tree.column(self.columns[-1]["key"], stretch=False, anchor="center")

    # ------------------------------------------------------
    # Click handler
    def _on_cell_click(self, row_id, col_key):
        if not row_id or col_key != "accion":
            return
        prestamo_id = self._rows_index.get(row_id)
        if not prestamo_id:
            return

        # Tomar datos para el mensaje
        session = self.session
        p = session.query(Prestamo).get(prestamo_id)
        if not p:
            return

        dni = p.socio.dni if p.socio else "?"
        resp = safe_messagebox(
            title="Confirmación",
            message=f"Se cerrará el préstamo con id {prestamo_id} del socio {dni}.\n\n¿Confirmar?",
            level="warning",
            buttons="okcancel",
            parent=self
        )

        if resp != "Aceptar":
            return

        # Cerrar préstamo (fecha_devolucion = hoy)
        p.fecha_devolucion = datetime.now()
        if p.ejemplar:
            p.ejemplar.disponible = True

        try:
            session.add(p)
            session.commit()
        except Exception:
            session.rollback()
            safe_messagebox(title="Error", message="No se pudo cerrar el préstamo.", level="error", buttons="ok", parent=self)
            return

        # Quitar fila de la vista (ya no está activo)
        self.table.tree.delete(row_id)

    # ------------------------------------------------------
    @staticmethod
    def _fmt_fecha(dttm):
        if not dttm:
            return ""
        d = dttm.date() if hasattr(dttm, "date") else dttm
        return f"{d.day:02d}/{d.month:02d}/{d.year:04d}"


if __name__ == "__main__":
    app = LoanActiveList()
    app.mainloop()
