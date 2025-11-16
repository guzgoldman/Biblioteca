import re
from datetime import datetime
import customtkinter as ctk
from db.session_manager import SessionManager

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from vista.componentes.utils import safe_messagebox

from modelo.Socio import Socio


class EditUser(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Gestión de Socios - Biblioteca Pública")
        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)

        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self._build_form()
        self.mainloop()

    # ======================================================
    def _build_form(self):
        """Construye el formulario de alta/edición de socio."""
        form_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=2)

        # Título
        title = ctk.CTkLabel(
            form_frame, text="Gestión de Socio",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2C3E50"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos principales
        campos = [
            ("DNI:", ""),
            ("Nombre:", ""),
            ("Apellido:", ""),
            ("Correo electrónico:", ""),
            ("Teléfono:", "")
        ]
        self.entries = {}

        for i, (label, default) in enumerate(campos, start=1):
            lbl = ctk.CTkLabel(form_frame, text=label, font=ctk.CTkFont(size=14), text_color="#2C3E50")
            lbl.grid(row=i, column=0, sticky="e", pady=6, padx=5)

            entry = ctk.CTkEntry(form_frame, width=250)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            self.entries[label] = entry

        # Estado
        estado_label = ctk.CTkLabel(form_frame, text="Estado:", font=ctk.CTkFont(size=14), text_color="#2C3E50")
        estado_label.grid(row=6, column=0, sticky="e", pady=6, padx=5)

        self.estado_var = ctk.StringVar(value="Activo")
        self.rb_activo = ctk.CTkRadioButton(form_frame, text="Activo", variable=self.estado_var, value="Activo")
        self.rb_inactivo = ctk.CTkRadioButton(form_frame, text="Inactivo", variable=self.estado_var, value="Inactivo")
        self.rb_activo.grid(row=6, column=1, sticky="w", padx=(0, 80), pady=4)
        self.rb_inactivo.grid(row=6, column=1, sticky="w", padx=(100, 0), pady=4)

        # Fechas (siempre deshabilitadas)
        fecha_alta_label = ctk.CTkLabel(form_frame, text="Fecha de alta:", font=ctk.CTkFont(size=14), text_color="#2C3E50")
        fecha_alta_label.grid(row=7, column=0, sticky="e", pady=6, padx=5)
        self.entry_fecha_alta = ctk.CTkEntry(form_frame, width=150, state="disabled")
        self.entry_fecha_alta.grid(row=7, column=1, sticky="w", pady=6, padx=5)

        fecha_baja_label = ctk.CTkLabel(form_frame, text="Fecha de baja:", font=ctk.CTkFont(size=14), text_color="#2C3E50")
        fecha_baja_label.grid(row=8, column=0, sticky="e", pady=6, padx=5)
        self.entry_fecha_baja = ctk.CTkEntry(form_frame, width=150, state="disabled")
        self.entry_fecha_baja.grid(row=8, column=1, sticky="w", pady=6, padx=5)

        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=(20, 10))

        self.btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", fg_color="#2ECC71",
                                         hover_color="#27AE60", width=120, command=self._guardar_usuario)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(btn_frame, text="Limpiar", fg_color="#E67E22",
                                         hover_color="#CA6F1E", width=120, command=self._limpiar_form)
        self.btn_limpiar.pack(side="left", padx=10)

        # Estado inicial
        self._set_fields_state("disabled")
        self.entries["DNI:"].configure(state="normal")

        # Validaciones dinámicas
        self.entries["DNI:"].bind("<FocusOut>", lambda e: self._check_dni())
        self.entries["DNI:"].bind("<Return>", lambda e: self._check_dni())
        for key in ["Nombre:", "Apellido:", "Correo electrónico:", "Teléfono:"]:
            self.entries[key].bind("<FocusOut>", lambda e, k=key: self._validate_field(k))

    # ======================================================
    def _validate_field(self, key):
        entry = self.entries[key]
        value = entry.get().strip()
        valid = True

        if key == "DNI:":
            valid = value.isdigit() and len(value) == 8
        elif key in ["Nombre:", "Apellido:"]:
            valid = bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{4,}$", value))
        elif key == "Teléfono:":
            valid = value.isdigit() and len(value) == 10
        elif key == "Correo electrónico:":
            valid = "@" in value and "." in value.split("@")[-1]

        entry.configure(border_color="#27AE60" if valid else "#E74C3C")

    # ======================================================
    def _set_fields_state(self, state):
        """Habilita/deshabilita campos pero nunca toca las fechas"""
        for label, entry in self.entries.items():
            if label != "DNI:":
                entry.configure(state=state)

        for widget in [self.rb_activo, self.rb_inactivo]:
            widget.configure(state=state)

        # FECHAS: siempre deshabilitadas
        self.entry_fecha_alta.configure(state="disabled")
        self.entry_fecha_baja.configure(state="disabled")

        self.btn_guardar.configure(state=state)

    # ======================================================
    def _check_dni(self):
        dni_entry = self.entries["DNI:"]
        dni = dni_entry.get().strip()

        if not dni:
            self._limpiar_form()
            return

        self._validate_field("DNI:")

        if not dni.isdigit() or len(dni) != 8:
            safe_messagebox(title="Error", message="El DNI debe contener exactamente 8 dígitos.", level="error", parent=self)
            return

        dni_entry.configure(state="disabled")
        socio = self.session.query(Socio).filter_by(dni=dni).first()
        self._set_fields_state("normal")

        if socio:
            self.entries["Nombre:"].delete(0, "end")
            self.entries["Apellido:"].delete(0, "end")
            self.entries["Correo electrónico:"].delete(0, "end")
            self.entries["Teléfono:"].delete(0, "end")

            self.entries["Nombre:"].insert(0, socio.nombre or "")
            self.entries["Apellido:"].insert(0, socio.apellido or "")
            self.entries["Correo electrónico:"].insert(0, socio.email or "")
            self.entries["Teléfono:"].insert(0, socio.celular or "")

            self.estado_var.set("Activo" if socio.activo else "Inactivo")

            self.entry_fecha_alta.configure(state="normal")
            self.entry_fecha_alta.delete(0, "end")
            self.entry_fecha_alta.insert(0, socio.fecha_alta.strftime("%d/%m/%Y"))
            self.entry_fecha_alta.configure(state="disabled")

            self.entry_fecha_baja.configure(state="normal")
            self.entry_fecha_baja.delete(0, "end")
            self.entry_fecha_baja.insert(0, socio.fecha_baja.strftime("%d/%m/%Y") if socio.fecha_baja else "")
            self.entry_fecha_baja.configure(state="disabled")

        else:
            self._clear_fields(except_dni=True)
            self._set_fields_state("normal")
            self.estado_var.set("Activo")

            self.entry_fecha_alta.configure(state="normal")
            self.entry_fecha_alta.delete(0, "end")
            self.entry_fecha_alta.insert(0, datetime.today().strftime("%d/%m/%Y"))
            self.entry_fecha_alta.configure(state="disabled")

            self.entry_fecha_baja.configure(state="normal")
            self.entry_fecha_baja.delete(0, "end")
            self.entry_fecha_baja.configure(state="disabled")

    # ======================================================
    def _limpiar_form(self):
        """Limpia todo el formulario dejando las fechas VACÍAS y deshabilitadas."""

        # Limpiar todos los campos editables
        for label, entry in self.entries.items():
            entry.configure(state="normal", border_color="#D0D3D4")
            entry.delete(0, "end")

        # Estado vuelve a Activo
        self.estado_var.set("Activo")

        # FECHAS → dejar VACÍAS (SIN FECHA), y deshabilitadas
        self.entry_fecha_alta.configure(state="normal")
        self.entry_fecha_alta.delete(0, "end")
        self.entry_fecha_alta.configure(state="disabled")

        self.entry_fecha_baja.configure(state="normal")
        self.entry_fecha_baja.delete(0, "end")
        self.entry_fecha_baja.configure(state="disabled")

        # Deshabilitar todos los campos excepto DNI
        self._set_fields_state("disabled")

        # DNI queda habilitado para ingresar otro
        self.entries["DNI:"].configure(state="normal", border_color="#D0D3D4")

    # ======================================================
    def _clear_fields(self, except_dni=False):
        for label, entry in self.entries.items():
            if except_dni and label == "DNI:":
                continue
            entry.delete(0, "end")

        self.estado_var.set("Activo")

        self.entry_fecha_baja.configure(state="normal")
        self.entry_fecha_baja.delete(0, "end")
        self.entry_fecha_baja.configure(state="disabled")

    # ======================================================
    def _guardar_usuario(self):
        dni = self.entries["DNI:"].get().strip()
        nombre = self.entries["Nombre:"].get().strip()
        apellido = self.entries["Apellido:"].get().strip()
        email = self.entries["Correo electrónico:"].get().strip()
        celular = self.entries["Teléfono:"].get().strip()
        estado = self.estado_var.get()

        # Validaciones
        if not dni.isdigit() or len(dni) != 8:
            safe_messagebox(title="Error", message="El DNI debe tener 8 dígitos.", level="error", parent=self)
            return

        patron_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{4,}$")
        if not patron_nombre.match(nombre) or not patron_nombre.match(apellido):
            safe_messagebox(title="Error", message="Nombre y apellido deben contener solo letras y mínimo 4 caracteres.",
                            level="error", parent=self)
            return

        if not celular.isdigit() or len(celular) != 10:
            safe_messagebox(title="Error", message="El teléfono debe tener 10 dígitos.", level="error", parent=self)
            return

        if email:
            if "@" not in email or "." not in email.split("@")[-1]:
                safe_messagebox(title="Error", message="Email inválido.", level="error", parent=self)
                return

        faltantes = {
            "DNI": dni,
            "Nombre": nombre,
            "Apellido": apellido,
            "Teléfono": celular,
            "Correo electrónico": email
        }
        missing = [k for k, v in faltantes.items() if not v]
        if missing:
            safe_messagebox(title="Error", message="Campos obligatorios faltantes:\n" + "\n".join(missing),
                            level="error", parent=self)
            return

        socio = self.session.query(Socio).filter_by(dni=dni).first()
        hoy = datetime.today().date()

        try:
            if socio:
                socio.nombre = nombre
                socio.apellido = apellido
                socio.email = email
                socio.celular = celular

                if estado == "Inactivo" and socio.activo:
                    socio.activo = False
                    socio.fecha_baja = hoy
                elif estado == "Activo" and not socio.activo:
                    socio.activo = True
                    socio.fecha_baja = None

                self.session.commit()
                safe_messagebox(title="Actualizado", message="Socio actualizado correctamente.", level="info", parent=self)

            else:
                if estado == "Inactivo":
                    safe_messagebox(title="Advertencia", message="Un socio nuevo no puede crearse como inactivo.",
                                    level="warning", parent=self)
                    return

                nuevo_socio = Socio(
                    dni=dni,
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    celular=celular,
                    activo=True,
                    fecha_alta=hoy,
                    fecha_baja=None
                )

                self.session.add(nuevo_socio)
                self.session.commit()

                safe_messagebox(title="Éxito", message="Socio registrado correctamente.", level="info", parent=self)

        except Exception as e:
            self.session.rollback()
            safe_messagebox(
                title="Error",
                message=f"Error al guardar el socio:\n{str(e)}",
                level="error", parent=self
            )
            return

        self._limpiar_form()