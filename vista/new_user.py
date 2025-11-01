import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from modelo.Socio import Socio


class NewUser(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Nuevo Usuario - Biblioteca Pública")

        callbacks = get_default_callbacks(self)

        # Layout base
        self.layout = AppLayout(self, banner_image="vistas/assets/banner.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        # Contenido del formulario
        self._build_form()

        self.mainloop()

    # ======================================================
    #   CONSTRUCCIÓN DEL FORMULARIO
    # ======================================================
    def _build_form(self):
        """Construye el formulario de alta de usuario."""
        form_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(
            form_frame,
            text="Alta de Nuevo Usuario",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2C3E50"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        campos = [
            ("Nombre:", ""),
            ("Apellido:", ""),
            ("DNI:", ""),
            ("Correo electrónico:", ""),
            ("Teléfono:", ""),
        ]

        self.entries = {}

        for i, (label, default) in enumerate(campos, start=1):
            lbl = ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14), text_color="#2C3E50")
            lbl.grid(row=i, column=0, sticky="e", pady=6, padx=5)

            entry = ctk.CTkEntry(form_frame, width=250)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            self.entries[label] = entry

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=(20, 10))

        btn_guardar = ctk.CTkButton(
            btn_frame,
            text="Guardar",
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=120,
            command=self._guardar_usuario
        )
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            fg_color="#E74C3C",
            hover_color="#922B21",
            width=120,
            command=self._go_dashboard
        )
        btn_cancelar.pack(side="left", padx=10)

    # ======================================================
    #   GUARDAR NUEVO USUARIO
    # ======================================================
    def _guardar_usuario(self):
        """Guarda los datos del nuevo usuario en la base."""
        session = self.layout.session

        # Forzar refresco de la sesión
        session.expire_all()

        dni = self.entries["DNI:"].get().strip()
        nombre = self.entries["Nombre:"].get().strip()
        apellido = self.entries["Apellido:"].get().strip()

        # Validar campos
        if not dni or not nombre or not apellido:
            CTkMessagebox(title="Error", message="Todos los campos obligatorios deben completarse.", icon="cancel")
            return

        # Comprobar si el socio ya existe
        exist = Socio.obtener_por_dni(session, dni)
        if exist:
            CTkMessagebox(title="Error", message=f"El DNI {dni} ya existe.", icon="cancel")
            return

        # Intentar crear el nuevo socio
        try:
            Socio.crear(session, dni=dni, nombre=nombre, apellido=apellido, commit=True)
            CTkMessagebox(title="Éxito", message=f"Socio {nombre} {apellido} agregado correctamente.")
            self._go_dashboard()
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error inesperado", message=str(e), icon="cancel")

    # ======================================================
    #   VOLVER AL DASHBOARD
    # ======================================================
    def _go_dashboard(self):
        """Regresa al dashboard."""
        self.destroy()
        from main_dashboard import MainDashboard
        MainDashboard()