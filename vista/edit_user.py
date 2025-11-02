import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from modelo.Socio import Socio
from datetime import datetime
import re


class EditUser(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Gestión de Socios - Biblioteca Pública")
        self.session = session
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

        title = ctk.CTkLabel(form_frame, text="Gestión de Socio", 
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#2C3E50")
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

        # Fechas
        fecha_alta_label = ctk.CTkLabel(form_frame, text="Fecha de alta:", font=ctk.CTkFont(size=14), text_color="#2C3E50")
        fecha_alta_label.grid(row=7, column=0, sticky="e", pady=6, padx=5)
        self.entry_fecha_alta = ctk.CTkEntry(form_frame, width=150)
        self.entry_fecha_alta.grid(row=7, column=1, sticky="w", pady=6, padx=5)

        fecha_baja_label = ctk.CTkLabel(form_frame, text="Fecha de baja:", font=ctk.CTkFont(size=14), text_color="#2C3E50")
        fecha_baja_label.grid(row=8, column=0, sticky="e", pady=6, padx=5)
        self.entry_fecha_baja = ctk.CTkEntry(form_frame, width=150)
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
        """Valida visualmente un campo individual."""
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

        # Colorear borde del campo
        entry.configure(border_color="#27AE60" if valid else "#E74C3C")

    # ======================================================
    def _set_fields_state(self, state):
        for label, entry in self.entries.items():
            if label != "DNI:":
                entry.configure(state=state)
        for widget in [self.rb_activo, self.rb_inactivo, self.entry_fecha_alta, self.entry_fecha_baja]:
            widget.configure(state=state)
        self.btn_guardar.configure(state=state)

    # ======================================================
    def _check_dni(self):
        """Valida o busca el socio según el DNI ingresado."""
        dni_entry = self.entries["DNI:"]
        dni = dni_entry.get().strip()

        if not dni:
            self._limpiar_form()
            return

        # Validación visual de DNI
        self._validate_field("DNI:")
        if not dni.isdigit() or len(dni) != 8:
            CTkMessagebox(title="Error", message="El DNI debe contener exactamente 8 dígitos numéricos.", icon="cancel")
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
            self.entry_fecha_alta.delete(0, "end")
            self.entry_fecha_alta.insert(0, socio.fecha_alta.strftime("%d/%m/%Y") if socio.fecha_alta else "")
            self.entry_fecha_baja.delete(0, "end")
            self.entry_fecha_baja.insert(0, socio.fecha_baja.strftime("%d/%m/%Y") if socio.fecha_baja else "")
        else:
            self._clear_fields(except_dni=True)
            self._set_fields_state("normal")
            self.estado_var.set("Activo")
            self.entry_fecha_alta.delete(0, "end")
            self.entry_fecha_alta.insert(0, datetime.today().strftime("%d/%m/%Y"))
            self.entry_fecha_baja.delete(0, "end")

    # ======================================================
    def _limpiar_form(self):
        """Limpia todo el formulario y reactiva el campo DNI."""
        for label, entry in self.entries.items():
            entry.configure(state="normal", border_color="#D0D3D4")
            entry.delete(0, "end")

        self.estado_var.set("Activo")
        self.entry_fecha_alta.delete(0, "end")
        self.entry_fecha_alta.insert(0, datetime.today().strftime("%d/%m/%Y"))
        self.entry_fecha_baja.delete(0, "end")

        self._set_fields_state("disabled")
        self.entries["DNI:"].configure(state="normal", border_color="#D0D3D4")

    # ======================================================
    def _clear_fields(self, except_dni=False):
        for label, entry in self.entries.items():
            if except_dni and label == "DNI:":
                continue
            entry.delete(0, "end")
        self.estado_var.set("Activo")
        self.entry_fecha_baja.delete(0, "end")

    # ======================================================
    def _guardar_usuario(self):
        """Guarda o actualiza un socio existente según el DNI ingresado."""
        dni = self.entries["DNI:"].get().strip()
        nombre = self.entries["Nombre:"].get().strip()
        apellido = self.entries["Apellido:"].get().strip()
        email = self.entries["Correo electrónico:"].get().strip()
        celular = self.entries["Teléfono:"].get().strip()
        estado = self.estado_var.get()

        # ======================================================
        # 🔹 VALIDACIONES DE FORMATO
        # ======================================================

        # DNI: solo números, longitud 8
        if not dni.isdigit() or len(dni) != 8:
            CTkMessagebox(title="Error", message="El DNI debe contener exactamente 8 dígitos numéricos.", icon="cancel")
            return

        # Nombre y apellido: letras y apóstrofo, longitud mínima 4
        patron_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{4,}$")
        if not patron_nombre.match(nombre):
            CTkMessagebox(
                title="Error",
                message="El nombre solo puede contener letras y debe tener al menos 4 caracteres.",
                icon="cancel"
            )
            return
        if not patron_nombre.match(apellido):
            CTkMessagebox(
                title="Error",
                message="El apellido solo puede contener letras (se permite apóstrofo) y debe tener al menos 4 caracteres.",
                icon="cancel"
            )
            return

        # Celular: obligatorio, solo números, longitud 10
        if not celular.isdigit() or len(celular) != 10:
            CTkMessagebox(title="Error", message="El número de teléfono debe tener exactamente 10 dígitos numéricos.", icon="cancel")
            return

        # Email: estructura básica "parte1@parte2", parte2 debe contener un punto
        if email:
            if "@" not in email or "." not in email.split("@")[-1]:
                CTkMessagebox(title="Error", message="El correo electrónico no tiene un formato válido.", icon="cancel")
                return

        # ======================================================
        # 🔹 VALIDACIONES DE CAMPOS OBLIGATORIOS
        # ======================================================
        campos_obligatorios = {
            "DNI": dni,
            "Nombre": nombre,
            "Apellido": apellido,
            "Teléfono": celular,
            "Correo electrónico": email
        }
        faltantes = [campo for campo, valor in campos_obligatorios.items() if not valor]
        if faltantes:
            CTkMessagebox(
                title="Error",
                message=f"Los siguientes campos son obligatorios:\n\n- " + "\n- ".join(faltantes),
                icon="cancel"
            )
            return

        # ======================================================
        # 🔹 OPERACIÓN DE GUARDADO / ACTUALIZACIÓN
        # ======================================================
        socio = self.session.query(Socio).filter_by(dni=dni).first()
        hoy = datetime.today().date()

        try:
            if socio:
                # 🔸 EDICIÓN
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
                CTkMessagebox(title="Actualizado", message="Socio actualizado correctamente.", icon="check")

            else:
                # 🔸 NUEVO REGISTRO
                if estado == "Inactivo":
                    CTkMessagebox(
                        title="Advertencia",
                        message="No se puede crear un nuevo socio como inactivo.",
                        icon="warning"
                    )
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
                CTkMessagebox(title="Éxito", message="Socio registrado correctamente.", icon="check")

        except Exception as e:
            self.session.rollback()
            CTkMessagebox(
                title="Error",
                message=f"Ocurrió un error al guardar el socio:\n\n{str(e)}",
                icon="cancel"
            )
            return

        # Limpia el formulario después del guardado
        self._limpiar_form()
