import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from modelo.Socio import Socio  # Ajustá la importación según tu estructura real


class EditBook(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Editar Libro - Biblioteca Pública")

        callbacks = get_default_callbacks(self)

        # Layout base
        self.layout = AppLayout(self, banner_image="vistas/assets/banner.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        # Contenido principal
        self._build_search_form()

        self.mainloop()

    # ======================================================
    def _build_search_form(self):
        """Primera vista: solo campo DNI + botón Buscar."""
        self.form_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(self.form_frame, text="Buscar Socio por DNI",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#2C3E50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        lbl_dni = ctk.CTkLabel(self.form_frame, text="DNI:", font=ctk.CTkFont(size=14))
        lbl_dni.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.entry_dni = ctk.CTkEntry(self.form_frame, width=200)
        self.entry_dni.grid(row=1, column=1, sticky="w", padx=5, pady=10)

        btn_buscar = ctk.CTkButton(self.form_frame, text="Buscar", width=120,
                                   fg_color="#3498DB", hover_color="#21618C",
                                   command=self._buscar_socio)
        btn_buscar.grid(row=2, column=0, columnspan=2, pady=15)

    # ======================================================
    def _buscar_socio(self):
        """Busca el socio por DNI y muestra los campos si existe."""
        dni = self.entry_dni.get().strip()

        if not dni:
            CTkMessagebox(title="Error", message="Debe ingresar un DNI.", icon="cancel")
            return

        socio = Socio.obtener_por_dni(dni)  # Método que debería retornar un dict o None

        if not socio:
            CTkMessagebox(title="No encontrado", message="No existe un socio con ese DNI.", icon="info")
            return

        # Limpia el frame actual y muestra el formulario de edición
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        self._build_edit_form(socio)

    # ======================================================
    def _build_edit_form(self, socio):
        """Construye el formulario con los datos del socio encontrado."""
        title = ctk.CTkLabel(self.form_frame, text=f"Editar Socio (DNI: {socio['dni']})",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#2C3E50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        campos = [
            ("Nombre:", socio["nombre"]),
            ("Apellido:", socio["apellido"]),
            ("Dirección:", socio["direccion"]),
            ("Email:", socio["email"] or ""),
            ("Celular:", socio["celular"] or "")
        ]

        self.entries = {}

        for i, (label, value) in enumerate(campos, start=1):
            lbl = ctk.CTkLabel(self.form_frame, text=label, font=ctk.CTkFont(size=14))
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=6)

            entry = ctk.CTkEntry(self.form_frame, width=250)
            entry.insert(0, value)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=6)
            self.entries[label] = entry

        # Botones inferiores
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=(20, 10))

        btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", fg_color="#2ECC71",
                                    hover_color="#27AE60", width=120,
                                    command=lambda: self._guardar_cambios(socio["dni"]))
        btn_guardar.pack(side="left", padx=10)

        btn_baja = ctk.CTkButton(btn_frame, text="Dar de baja", fg_color="#E67E22",
                                 hover_color="#CA6F1E", width=120,
                                 command=lambda: self._dar_de_baja(socio["dni"]))
        btn_baja.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#E74C3C",
                                     hover_color="#922B21", width=120,
                                     command=self._go_dashboard)
        btn_cancelar.pack(side="left", padx=10)

    # ======================================================
    def _guardar_cambios(self, dni):
        """Guarda los cambios del socio."""
        datos = {lbl: entry.get() for lbl, entry in self.entries.items()}
        print(f"Actualizando socio {dni} con datos:", datos)
        # Socio.actualizar(dni, datos)
        CTkMessagebox(title="Éxito", message="Los datos fueron actualizados correctamente.", icon="check")

    def _dar_de_baja(self, dni):
        """Da de baja el socio."""
        respuesta = CTkMessagebox(title="Confirmar baja",
                                  message=f"¿Seguro que desea dar de baja al socio {dni}?",
                                  icon="warning", option_1="Sí", option_2="No").get()
        if respuesta == "Sí":
            # Socio.eliminar(dni)
            CTkMessagebox(title="Baja realizada", message="El socio ha sido eliminado.", icon="check")
            self._go_dashboard()

    def _go_dashboard(self):
        """Regresa al dashboard."""
        self.destroy()
        from main_dashboard import MainDashboard
        MainDashboard()