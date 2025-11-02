import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from modelo.Ejemplar import Ejemplar


class EditCopy(BaseApp):
    def __init__(self, session=None, isbn=None, admin=None):
        super().__init__(title="Editar Ejemplar - Biblioteca Pública")
        self.session = session
        self.admin = admin
        self.isbn = (isbn or "").upper()  # 🔹 Forzar a mayúsculas

        callbacks = get_default_callbacks(self)
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        self._build_form()
        self._load_ejemplares()
        self.mainloop()

    # ======================================================
    def _build_form(self):
        frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(frame, text="Editar ejemplar",
                             font=ctk.CTkFont(size=22, weight="bold"),
                             text_color="#2C3E50")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Selector de ejemplar
        ctk.CTkLabel(frame, text="Seleccionar ejemplar:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="e", pady=6, padx=5)
        self.ejemplar_cb = ctk.CTkComboBox(frame, values=[], width=250, command=self._on_select_ejemplar)
        self.ejemplar_cb.grid(row=1, column=1, sticky="w", pady=6, padx=5)

        # Campos
        campos = [
            ("Código:", False),
            ("Libro ISBN:", False),
            ("Número ejemplar:", False),
            ("Disponible:", False),
            ("Alta ejemplar:", False),
            ("Baja ejemplar:", False)
        ]
        self.entries = {}

        for i, (label, editable) in enumerate(campos, start=2):
            ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=14)).grid(row=i, column=0, sticky="e", pady=6, padx=5)
            entry = ctk.CTkEntry(frame, width=250)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            entry.configure(state="normal" if editable else "readonly")
            self.entries[label] = entry

        # Estado (Activo / Inactivo)
        estado_label = ctk.CTkLabel(frame, text="Estado:", font=ctk.CTkFont(size=14))
        estado_label.grid(row=8, column=0, sticky="e", pady=6, padx=5)
        self.estado_var = ctk.StringVar(value="Activo")
        self.rb_activo = ctk.CTkRadioButton(frame, text="Activo", variable=self.estado_var, value="Activo")
        self.rb_inactivo = ctk.CTkRadioButton(frame, text="Inactivo", variable=self.estado_var, value="Inactivo")
        self.rb_activo.grid(row=8, column=1, sticky="w", padx=(0, 80), pady=4)
        self.rb_inactivo.grid(row=8, column=1, sticky="w", padx=(100, 0), pady=4)

        # Botones
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=(20, 10))

        self.btn_guardar = ctk.CTkButton(btn_frame, text="Guardar", fg_color="#2ECC71",
                                         hover_color="#27AE60", width=120, command=self._guardar_cambios)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_agregar = ctk.CTkButton(btn_frame, text="Agregar ejemplar", fg_color="#2980B9",
                                         hover_color="#21618C", width=160, command=self._agregar_ejemplar)
        self.btn_agregar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", fg_color="#E74C3C",
                                          hover_color="#922B21", width=120, command=self._volver)
        self.btn_cancelar.pack(side="left", padx=10)

    # ======================================================
    def _load_ejemplares(self):
        """Carga los ejemplares del libro actual en el ComboBox."""
        if not self.isbn:
            CTkMessagebox(title="Error", message="No se recibió ISBN para cargar ejemplares.", icon="cancel")
            return

        ejemplares = (
            self.session.query(Ejemplar)
            .filter_by(libro_isbn=self.isbn)
            .order_by(Ejemplar.numero_ejemplar)
            .all()
        )

        if not ejemplares:
            CTkMessagebox(title="Aviso", message="No hay ejemplares asociados a este libro.", icon="info")
            return

        self.ejemplares = ejemplares
        self.ejemplar_cb.configure(values=[e.codigo for e in ejemplares])
        if ejemplares:
            self.ejemplar_cb.set(ejemplares[0].codigo)
            self._load_data(ejemplares[0])

    # ======================================================
    def _on_select_ejemplar(self, codigo):
        ejemplar = next((e for e in self.ejemplares if e.codigo == codigo), None)
        if ejemplar:
            self._load_data(ejemplar)

    # ======================================================
    def _load_data(self, ejemplar):
        """Llena los campos con los datos del ejemplar seleccionado."""
        self.entries["Código:"].configure(state="normal")
        self.entries["Código:"].delete(0, "end")
        self.entries["Código:"].insert(0, ejemplar.codigo)
        self.entries["Código:"].configure(state="readonly")

        self.entries["Libro ISBN:"].configure(state="normal")
        self.entries["Libro ISBN:"].delete(0, "end")
        self.entries["Libro ISBN:"].insert(0, (ejemplar.libro_isbn or "").upper())  # 🔹 siempre en mayúsculas
        self.entries["Libro ISBN:"].configure(state="readonly")

        self.entries["Número ejemplar:"].configure(state="normal")
        self.entries["Número ejemplar:"].delete(0, "end")
        self.entries["Número ejemplar:"].insert(0, ejemplar.numero_ejemplar)
        self.entries["Número ejemplar:"].configure(state="readonly")

        self.entries["Disponible:"].configure(state="normal")
        self.entries["Disponible:"].delete(0, "end")
        self.entries["Disponible:"].insert(0, "Sí" if ejemplar.disponible else "No")
        self.entries["Disponible:"].configure(state="readonly")

        self.entries["Alta ejemplar:"].configure(state="normal")
        self.entries["Alta ejemplar:"].delete(0, "end")
        self.entries["Alta ejemplar:"].insert(0, ejemplar.alta_ejemplar.strftime("%d/%m/%Y") if ejemplar.alta_ejemplar else "")
        self.entries["Alta ejemplar:"].configure(state="readonly")

        self.entries["Baja ejemplar:"].configure(state="normal")
        self.entries["Baja ejemplar:"].delete(0, "end")
        self.entries["Baja ejemplar:"].insert(0, ejemplar.baja_ejemplar.strftime("%d/%m/%Y") if ejemplar.baja_ejemplar else "")
        self.entries["Baja ejemplar:"].configure(state="readonly")

        # 🔹 Estado depende de si tiene fecha de baja
        self.estado_var.set("Inactivo" if ejemplar.baja_ejemplar else "Activo")
        self.ejemplar_actual = ejemplar

    # ======================================================
    def _agregar_ejemplar(self):
        """Crea un nuevo ejemplar para el libro actual."""
        if not self.isbn:
            CTkMessagebox(title="Error", message="No hay un ISBN válido para crear ejemplar.", icon="cancel")
            return

        isbn_mayus = self.isbn.upper()  # 🔹 Forzar ISBN en mayúsculas

        ultimo = (
            self.session.query(Ejemplar)
            .filter_by(libro_isbn=isbn_mayus)
            .order_by(Ejemplar.numero_ejemplar.desc())
            .first()
        )
        if not ultimo:
            CTkMessagebox(title="Error", message="No hay ejemplares base para generar el código.", icon="cancel")
            return

        nuevo_numero = ultimo.numero_ejemplar + 1
        base_code = ultimo.codigo.rsplit("-", 1)[0] if "-" in ultimo.codigo else ultimo.codigo
        nuevo_codigo = f"{base_code}-{nuevo_numero}"

        nuevo = Ejemplar(
            codigo=nuevo_codigo,
            numero_ejemplar=nuevo_numero,
            disponible=True,
            libro_isbn=isbn_mayus,
            alta_ejemplar=datetime.today().date(),
            baja_ejemplar=None,
        )

        try:
            self.session.add(nuevo)
            self.session.commit()
            CTkMessagebox(title="Éxito", message=f"Ejemplar {nuevo_codigo} agregado correctamente.", icon="check")
            self._load_ejemplares()
            self.ejemplar_cb.set(nuevo_codigo)
            self._load_data(nuevo)
        except Exception as e:
            self.session.rollback()
            CTkMessagebox(title="Error", message=f"No se pudo crear el ejemplar:\n{str(e)}", icon="cancel")

    # ======================================================
    def _guardar_cambios(self):
        """Guarda cambios del ejemplar actual."""
        if not hasattr(self, "ejemplar_actual"):
            CTkMessagebox(title="Error", message="No hay ejemplar cargado.", icon="cancel")
            return

        ejemplar = self.ejemplar_actual

        # No se puede guardar como inactivo si fue recién creado
        if ejemplar.alta_ejemplar:
            alta_date = ejemplar.alta_ejemplar.date() if isinstance(ejemplar.alta_ejemplar, datetime) else ejemplar.alta_ejemplar
            if (datetime.today().date() - alta_date).days <= 0 and self.estado_var.get() == "Inactivo":
                CTkMessagebox(title="Error", message="No se puede dar de baja un ejemplar recién creado.", icon="cancel")
                return


        try:
            if self.estado_var.get() == "Inactivo" and ejemplar.baja_ejemplar is None:
                ejemplar.baja_ejemplar = datetime.today().date()
            elif self.estado_var.get() == "Activo" and ejemplar.baja_ejemplar is not None:
                ejemplar.baja_ejemplar = None

            self.session.commit()
            CTkMessagebox(title="Éxito", message="Ejemplar actualizado correctamente.", icon="check")
            self._load_ejemplares()
        except Exception as e:
            self.session.rollback()
            CTkMessagebox(title="Error", message=f"No se pudo actualizar el ejemplar:\n{str(e)}", icon="cancel")

    # ======================================================
    def _volver(self):
        """Vuelve a la vista anterior."""
        self.destroy()
        from vista.edit_book import NewBook
        NewBook(session=self.session, admin=self.admin)
