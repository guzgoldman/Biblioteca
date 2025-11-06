import re
import customtkinter as ctk
from db.session_manager import SessionManager

from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from vista.componentes.utils import safe_messagebox   # ✅ Nuevo helper seguro

from modelo.Libro import Libro
from modelo.Ejemplar import Ejemplar
from modelo.Categoria import Categoria


class EditBook(BaseApp):
    def __init__(self, session=None, admin=None):
        super().__init__(title="Gestión de Libros - Biblioteca Pública")
        self.session = session or SessionManager.get_session()
        self.admin = admin

        callbacks = get_default_callbacks(self)
        self.layout = AppLayout(
            self,
            banner_image="vista/images/banner_bandera.jpg",
            callbacks=callbacks
        )
        self.layout.pack(fill="both", expand=True)

        self._build_form()
        self.mainloop()

    # ======================================================
    def _build_form(self):
        """Construye el formulario de alta/edición de libro."""
        frame = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(
            frame,
            text="Gestión de Libros",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2C3E50"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campos
        campos = [
            ("ISBN:", ""),
            ("Título:", ""),
            ("Autor:", ""),
            ("Código ejemplares:", "")
        ]
        self.entries = {}
        for i, (label, default) in enumerate(campos, start=1):
            ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, sticky="e", pady=6, padx=5
            )
            entry = ctk.CTkEntry(frame, width=250)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky="w", pady=6, padx=5)
            self.entries[label] = entry

        # Categoría
        ctk.CTkLabel(frame, text="Categoría:", font=ctk.CTkFont(size=14)).grid(
            row=5, column=0, sticky="e", pady=6, padx=5
        )
        categorias = [c.nombre for c in self.session.query(Categoria).order_by(Categoria.nombre).all()]
        self.categoria_cb = ctk.CTkComboBox(frame, values=categorias or ["Sin categorías"], width=250)
        self.categoria_cb.grid(row=5, column=1, sticky="w", pady=6, padx=5)

        # Cantidad de ejemplares
        ctk.CTkLabel(frame, text="Cantidad de ejemplares:", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, sticky="e", pady=6, padx=5
        )
        self.cantidad_cb = ctk.CTkComboBox(frame, values=[str(i) for i in range(1, 16)], width=100)
        self.cantidad_cb.set("1")
        self.cantidad_cb.grid(row=6, column=1, sticky="w", pady=6, padx=5)

        # Botones
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=(20, 10))

        self.btn_guardar = ctk.CTkButton(
            btn_frame,
            text="Guardar",
            fg_color="#2ECC71",
            hover_color="#27AE60",
            width=120,
            command=self._guardar_libro
        )
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_editar_ejemplares = ctk.CTkButton(
            btn_frame,
            text="Editar ejemplares",
            fg_color="#2980B9",
            hover_color="#21618C",
            width=160,
            command=self._abrir_edit_copy,
            state="disabled"
        )
        self.btn_editar_ejemplares.pack(side="left", padx=10)

        self.btn_limpiar = ctk.CTkButton(
            btn_frame,
            text="Limpiar",
            fg_color="#E67E22",
            hover_color="#CA6F1E",
            width=120,
            command=self._limpiar_form
        )
        self.btn_limpiar.pack(side="left", padx=10)

        # Estado inicial
        self._set_fields_state("disabled")
        self.entries["ISBN:"].configure(state="normal")

        # Evento ISBN
        self.entries["ISBN:"].bind("<FocusOut>", lambda e: self._check_isbn())
        self.entries["ISBN:"].bind("<Return>", lambda e: self._check_isbn())

    # ======================================================
    def _set_fields_state(self, state):
        for label, entry in self.entries.items():
            if label != "ISBN:":
                entry.configure(state=state)
        for widget in [self.categoria_cb, self.cantidad_cb, self.btn_guardar]:
            widget.configure(state=state)

    # ======================================================
    def _check_isbn(self):
        isbn = self.entries["ISBN:"].get().strip()
        if not isbn:
            self._limpiar_form()
            return

        if not re.match(r"^[0-9A-Za-z\-]{8,20}$", isbn):
            safe_messagebox(title="Error", message="El ISBN no tiene un formato válido.", level="error", buttons="ok", parent=self)
            return

        self.entries["ISBN:"].configure(state="disabled")
        libro = self.session.query(Libro).filter_by(isbn=isbn).first()
        self._set_fields_state("normal")

        if libro:
            # Cargar datos
            for campo in ["Título:", "Autor:", "Código ejemplares:"]:
                self.entries[campo].delete(0, "end")

            self.entries["Título:"].insert(0, libro.titulo)
            self.entries["Autor:"].insert(0, libro.autor)

            primer = self.session.query(Ejemplar).filter_by(libro_isbn=isbn).first()
            if primer:
                base_code = primer.codigo.rsplit("-", 1)[0] if "-" in primer.codigo else primer.codigo
                self.entries["Código ejemplares:"].insert(0, base_code)

            if libro.categorias:
                self.categoria_cb.set(libro.categorias[0].nombre)

            cantidad = self.session.query(Ejemplar).filter_by(libro_isbn=isbn).count()
            self.cantidad_cb.set(str(cantidad))
            self.btn_editar_ejemplares.configure(state="normal")

        else:
            self._clear_fields(except_isbn=True)
            self._set_fields_state("normal")
            self.btn_editar_ejemplares.configure(state="disabled")

    # ======================================================
    def _abrir_edit_copy(self):
        isbn = self.entries["ISBN:"].get().strip()
        if not isbn:
            safe_messagebox(title="Error", message="Debe tener un libro cargado para editar ejemplares.", level="error", buttons="ok", parent=self)
            return

        self.destroy()
        from vista.edit_copy import EditCopy
        EditCopy(session=self.session, isbn=isbn, admin=self.admin)

    # ======================================================
    def _guardar_libro(self):
        isbn = self.entries["ISBN:"].get().strip()
        titulo = self.entries["Título:"].get().strip()
        autor = self.entries["Autor:"].get().strip()
        codigo = self.entries["Código ejemplares:"].get().strip()
        categoria_nombre = self.categoria_cb.get()
        cantidad = int(self.cantidad_cb.get())

        if not isbn or not titulo or not autor or not codigo:
            safe_messagebox(title="Error", message="Todos los campos son obligatorios.", level="error", buttons="ok", parent=self)
            return

        libro = self.session.query(Libro).filter_by(isbn=isbn).first()
        try:
            if libro:
                libro.editar(
                    self.session,
                    nuevo_titulo=titulo,
                    nuevo_autor=autor,
                    nuevos_ejemplares=0,
                    codigo_identificador=codigo,
                    commit=True
                )
                ejemplares = self.session.query(Ejemplar).filter_by(libro_isbn=isbn).all()
                for ej in ejemplares:
                    if "-" in ej.codigo:
                        suf = ej.codigo.split("-")[-1]
                        ej.codigo = f"{codigo}-{suf}"
                    else:
                        ej.codigo = f"{codigo}"
                self.session.commit()
                safe_messagebox(title="Actualizado", message="Libro actualizado correctamente.", level="info", buttons="ok", parent=self)
            else:
                Libro.crear_con_ejemplares(
                    self.session,
                    titulo=titulo,
                    autor=autor,
                    isbn=isbn,
                    codigo_identificador=codigo,
                    cantidad_ejemplares=cantidad,
                    commit=True
                )
                safe_messagebox(title="Éxito", message="Libro creado correctamente.", level="info", buttons="ok", parent=self)
        except Exception as e:
            self.session.rollback()
            safe_messagebox(title="Error", message=f"No se pudo guardar el libro:\n{str(e)}", level="error", buttons="ok", parent=self)

        self._limpiar_form()

    # ======================================================
    def _clear_fields(self, except_isbn=False):
        for label, entry in self.entries.items():
            if except_isbn and label == "ISBN:":
                continue
            entry.delete(0, "end")

    # ======================================================
    def _limpiar_form(self):
        for entry in self.entries.values():
            entry.configure(state="normal")
            entry.delete(0, "end")
        self.categoria_cb.set("Sin categorías")
        self.cantidad_cb.set("1")
        self._set_fields_state("disabled")
        self.entries["ISBN:"].configure(state="normal")
        self.btn_editar_ejemplares.configure(state="disabled")