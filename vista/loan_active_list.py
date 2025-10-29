import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import customtkinter as ctk
from datetime import date
from componentes import AppLayout, BaseApp, Table, get_default_callbacks
from db.Conector import SessionLocal
from modelo.Prestamo import Prestamo

class LoanActiveList(BaseApp):
    def __init__(self):
        super().__init__(title="Biblioteca Pública - Préstamos Activos")

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
            text="Listado de Prestamos Activos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Definir columnas
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

        # Tabla reutilizable
        self.table = Table(self.content_frame, columns, width=900, height=420)
        self.table.grid(row=1, column=0, sticky="n")

        # Cargar datos
        self.load_data()

    

    def load_data(self):
        session = SessionLocal()
        activos = session.query(Prestamo).filter(Prestamo.fecha_devolucion == None).all()
        session.close()
        rows = []
        today = date.today()

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
                "fecha_solicitado": self.formato_fecha(p.fecha_prestamo),
                "fecha_devolucion": self.formato_fecha(p.fecha_devolucion_pactada),
                "estado": "Activo",
                "estado_bg": estado_bg,
            })
        self.table.set_data(rows)
    
    def formato_fecha(self,dttm):
        if not dttm:
            return ""
        d = dttm.date() if hasattr(dttm, "date") else dttm
        return f"{d.day:02d}/{d.month:02d}/{d.year:04d}"

def main():
    app = LoanActiveList()
    app.mainloop()

if __name__ == "__main__":
    main()