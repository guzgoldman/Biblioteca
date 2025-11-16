import customtkinter as ctk
from datetime import datetime, timedelta
from db.session_manager import SessionManager

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from vista.componentes.utils import safe_messagebox

from modelo.Socio import Socio
from modelo.Libro import Libro
from modelo.Ejemplar import Ejemplar
from modelo.Prestamo import Prestamo


class NewLoan(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Registrar Préstamo - Biblioteca Pública")
        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self._build_form()
        self.mainloop()

    # ======================================================
    def _build_form(self):
        """Construye el formulario de registro de préstamo."""
        frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(frame, text="Registrar Préstamo",
                             font=ctk.CTkFont(size=22, weight="bold"), text_color="#2C3E50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos base
        self.entries = {}

        campos = [
            ("DNI socio:", True),
            ("ISBN:", False),
            ("Título:", False),
            ("Autor:", False),
            ("Categoría:", False),
        ]

        for i, (label, editable) in enumerate(campos, start=1):
            lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=14))
            lbl.grid(row=i, column=0, sticky="e", pady=6, padx=5)
            entry = ctk.CTkEntry(frame, width=300)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            if not editable:
                entry.configure(state="disabled")
            self.entries[label] = entry

        # Dropdown ejemplares
        lbl_ejemplar = ctk.CTkLabel(frame, text="Ejemplar:", font=ctk.CTkFont(size=14))
        lbl_ejemplar.grid(row=6, column=0, sticky="e", pady=6, padx=5)
        self.cb_ejemplar = ctk.CTkComboBox(frame, values=[], width=300, state="disabled")
        self.cb_ejemplar.grid(row=6, column=1, sticky="w", pady=6, padx=5)

        # Dropdown días de préstamo
        lbl_dias = ctk.CTkLabel(frame, text="Días de préstamo:", font=ctk.CTkFont(size=14))
        lbl_dias.grid(row=7, column=0, sticky="e", pady=6, padx=5)
        self.cb_dias = ctk.CTkComboBox(frame, values=[str(i) for i in range(3, 11)], width=120, state="disabled")
        self.cb_dias.grid(row=7, column=1, sticky="w", pady=6, padx=5)
        self.cb_dias.set("3")

        # Fecha devolución
        lbl_dev = ctk.CTkLabel(frame, text="Fecha devolución:", font=ctk.CTkFont(size=14))
        lbl_dev.grid(row=8, column=0, sticky="e", pady=6, padx=5)
        self.entry_fecha_dev = ctk.CTkEntry(frame, width=150, state="disabled")
        self.entry_fecha_dev.grid(row=8, column=1, sticky="w", pady=6, padx=5)

        # Botones
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=(20, 10))

        self.btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", fg_color="#2ECC71",
                                         hover_color="#27AE60", width=120, command=self._guardar_prestamo, state="disabled")
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#E74C3C",
                                          hover_color="#922B21", width=120, command=self._volver)
        self.btn_cancelar.pack(side="left", padx=10)

        # Eventos reactivos
        self.entries["DNI socio:"].bind("<Return>", lambda e: self._buscar_socio())
        self.entries["ISBN:"].bind("<Return>", lambda e: self._buscar_libro())
        self.cb_dias.configure(command=lambda value: self._actualizar_fecha_devolucion())

    # ======================================================
    def _set_state(self, state_dict):
        """Activa/desactiva campos según el estado especificado."""
        for key, state in state_dict.items():
            if key in self.entries:
                self.entries[key].configure(state=state)
        self.cb_ejemplar.configure(state=state_dict.get("Ejemplar:", "disabled"))
        self.cb_dias.configure(state=state_dict.get("Días:", "disabled"))
        self.entry_fecha_dev.configure(state=state_dict.get("Fecha devolución:", "disabled"))
        self.btn_guardar.configure(state=state_dict.get("Guardar", "disabled"))

    # ======================================================
    def _buscar_socio(self):
        dni = self.entries["DNI socio:"].get().strip()
        if not dni:
            return

        socio = Socio.obtener_por_dni(self.session, dni)
        if not socio:
            safe_messagebox(title="Error", message="No se encontró ningún socio con ese DNI.", level="error", buttons="ok", parent=self)
            return

        # Verificar si tiene préstamo activo
        prestamo_activo = self.session.query(Prestamo).filter(
            Prestamo.socio_id == socio.dni,
            Prestamo.fecha_devolucion.is_(None)
        ).first()
        
        print(f"[DEBUG] Préstamo activo para socio {socio.dni}: {prestamo_activo}")

        if prestamo_activo:
            safe_messagebox(title="Aviso", message="Este socio ya posee un préstamo activo.", level="warning", buttons="ok", parent=self)
            return

        # Si todo OK → habilitar ISBN
        self.entries["ISBN:"].configure(state="normal")

    # ======================================================
    def _buscar_libro(self):
        isbn = self.entries["ISBN:"].get().strip().upper()
        if not isbn:
            return

        libro = self.session.query(Libro).filter_by(isbn=isbn).first()
        if not libro:
            safe_messagebox(title="Error", message="No se encontró un libro con ese ISBN.", level="error", buttons="ok", parent=self)
            return

        # Buscar ejemplares disponibles
        ejemplares_disp = (
            self.session.query(Ejemplar)
            .filter_by(libro_isbn=isbn, disponible=True, baja_ejemplar=None)
            .all()
        )

        if not ejemplares_disp:
            safe_messagebox(title="Aviso", message="No hay ejemplares disponibles de este libro.", level="warning", buttons="ok", parent=self)
            return

        # Cargar datos del libro
        self.entries["ISBN:"].delete(0, "end")
        self.entries["ISBN:"].insert(0, isbn)
        self.entries["Título:"].configure(state="normal")
        self.entries["Título:"].delete(0, "end")
        self.entries["Título:"].insert(0, libro.titulo)
        self.entries["Título:"].configure(state="disabled")

        self.entries["Autor:"].configure(state="normal")
        self.entries["Autor:"].delete(0, "end")
        self.entries["Autor:"].insert(0, libro.autor)
        self.entries["Autor:"].configure(state="disabled")

        categoria = libro.categorias[0].nombre if libro.categorias else "Sin categoría"
        self.entries["Categoría:"].configure(state="normal")
        self.entries["Categoría:"].delete(0, "end")
        self.entries["Categoría:"].insert(0, categoria)
        self.entries["Categoría:"].configure(state="disabled")

        # Cargar dropdown de ejemplares
        self.cb_ejemplar.configure(state="normal")
        self.cb_ejemplar.configure(values=[e.codigo for e in ejemplares_disp])
        self.cb_ejemplar.set(ejemplares_disp[0].codigo)

        # Activar préstamo
        self.cb_dias.configure(state="normal")
        self._actualizar_fecha_devolucion()
        self.btn_guardar.configure(state="normal")

    # ======================================================
    def _actualizar_fecha_devolucion(self):
        """Calcula la fecha de devolución en base a los días seleccionados y la muestra como no editable."""
        try:
            dias = int(self.cb_dias.get())
        except ValueError:
            return

        fecha_dev = datetime.today().date() + timedelta(days=dias)

        # Habilitar solo para escribir
        self.entry_fecha_dev.configure(state="normal")
        self.entry_fecha_dev.delete(0, "end")
        self.entry_fecha_dev.insert(0, fecha_dev.strftime("%d/%m/%Y"))
        # Volver a bloquear
        self.entry_fecha_dev.configure(state="disabled")


    # ======================================================
    def _guardar_prestamo(self):
        administrador_id=self.admin.dni if self.admin else None,
        dni = self.entries["DNI socio:"].get().strip()
        isbn = self.entries["ISBN:"].get().strip().upper()
        codigo_ejemplar = self.cb_ejemplar.get().strip()
        dias = int(self.cb_dias.get())
        fecha_dev = datetime.today().date() + timedelta(days=dias)

        if not (dni and isbn and codigo_ejemplar):
            safe_messagebox(title="Error", message="Complete todos los campos requeridos.", level="error", buttons="ok", parent=self)
            return

        socio = Socio.obtener_por_dni(self.session, dni)
        ejemplar = self.session.query(Ejemplar).filter_by(codigo=codigo_ejemplar).first()

        if not socio or not ejemplar:
            safe_messagebox(title="Error", message="Datos inválidos para socio o ejemplar.", level="error", buttons="ok", parent=self)
            return

        try:
            nuevo_prestamo = Prestamo(
                ejemplar_id=ejemplar.codigo,
                socio_id=socio.dni,
                administrador_id=self.admin.dni if self.admin else None,
                fecha_prestamo=datetime.today().date(),
                fecha_devolucion_pactada=fecha_dev
            )
            ejemplar.disponible = False

            self.session.add(nuevo_prestamo)
            self.session.commit()

            safe_messagebox(title="Éxito", message="Préstamo registrado correctamente.",  level="info", buttons="ok", parent=self)
            self._volver()
        except Exception as e:
            self.session.rollback()
            safe_messagebox(title="Error", message=f"No se pudo registrar el préstamo:\n{str(e)}", level="error", buttons="ok", parent=self)

    # ======================================================
    def _volver(self):
        """Vuelve al dashboard."""
        self.destroy()
        from vista.main_dashboard import MainDashboard
        MainDashboard(session=self.session, admin=self.admin)
