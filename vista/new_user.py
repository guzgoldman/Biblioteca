import customtkinter as ctk
from componentes import BaseApp, AppLayout, go_to_dashboard,go_to_users, go_to_books, go_to_loans, go_to_exit

class NewUser(BaseApp):
    def __init__(self):
        super().__init__(title="Nuevo Usuario - Biblioteca Pública")

        # Callbacks del menú lateral
        callbacks = {
            "Escritorio": self._go_dashboard,
            "Socios": go_to_users,  # Podrías agregar más vistas luego
            "Libros": go_to_books,
            "Préstamos": go_to_loans,
            "Salir": go_to_exit,
        }

        # Layout base
        self.layout = AppLayout(self, banner_image="vistas/assets/banner.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        # Contenido del formulario
        self._build_form()

        self.mainloop()

    def _build_form(self):
        """Construye el formulario de alta de usuario."""
        form_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(form_frame, text="Alta de Nuevo Usuario",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#2C3E50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos del formulario
        campos = [
            ("Nombre:", ""),
            ("Apellido:", ""),
            ("DNI:", ""),
            ("Correo electrónico:", ""),
            ("Teléfono:", ""),
        ]

        self.entries = {}

        for i, (label, default) in enumerate(campos, start=1):
            lbl = ctk.CTkLabel(form_frame, text=label,
                               font=ctk.CTkFont(size=14),
                               text_color="#2C3E50")
            lbl.grid(row=i, column=0, sticky="e", pady=6, padx=5)

            entry = ctk.CTkEntry(form_frame, width=250)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            self.entries[label] = entry

        # Botones inferiores
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=(20, 10))

        btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", fg_color="#2ECC71",
                                    hover_color="#27AE60", width=120,
                                    command=self._guardar_usuario)
        btn_guardar.pack(side="left", padx=10)

        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#E74C3C",
                                     hover_color="#922B21", width=120,
                                     command=self._go_dashboard)
        btn_cancelar.pack(side="left", padx=10)

    # ======================================================
    def _guardar_usuario(self):
        """Simula guardar datos del usuario."""
        datos = {lbl: entry.get() for lbl, entry in self.entries.items()}
        print("Datos del nuevo usuario:", datos)

    def _go_dashboard(self):
        """Regresa al dashboard."""
        self.destroy()
        from main_dashboard import MainDashboard
        MainDashboard()
