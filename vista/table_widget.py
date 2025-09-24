# table_widget.py (añade soporte para 'estado_bg')
import customtkinter as ctk

class Table(ctk.CTkFrame):
    def __init__(self, master, columns, data=None, on_row_click=None, height=380, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.columns = columns
        self._data = data or []
        self._sort_key = None
        self._sort_reverse = False
        self.on_row_click = on_row_click

        self.total_width = sum(col.get("width", 120) for col in columns) + (10 * (len(columns) - 1))

        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent", width=self.total_width)
        self.header.pack(pady=(0, 6))

        for col_idx, col in enumerate(self.columns):
            col_w = col.get("width", 120)
            btn = ctk.CTkButton(
                self.header,
                text=col.get("text", col["key"]),
                width=col_w,
                command=lambda k=col["key"]: self.sort_by(k),
                anchor="w"
            )
            btn.grid(row=0, column=col_idx, padx=(0, 10), sticky="w")
            self.header.grid_columnconfigure(col_idx, minsize=col_w, weight=0)

        # Body (no expand para que la scrollbar quede pegada)
        self.body = ctk.CTkScrollableFrame(self, width=self.total_width, height=height)
        self.body.pack(pady=0)

        for col_idx, col in enumerate(self.columns):
            col_w = col.get("width", 120)
            self.body.grid_columnconfigure(col_idx, minsize=col_w, weight=0)

        self.render_rows()

    def set_data(self, data):
        self._data = data or []
        self._sort_key = None
        self._sort_reverse = False
        self.render_rows()

    def sort_by(self, key):
        if self._sort_key == key:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_key = key
            self._sort_reverse = False

        def _safe(x):
            v = x.get(key, "")
            return "" if v is None else v
        self._data = sorted(self._data, key=_safe, reverse=self._sort_reverse)
        self.render_rows()

    def clear_rows(self):
        for w in self.body.winfo_children():
            w.destroy()

    def render_rows(self):
        self.clear_rows()
        for r, row in enumerate(self._data, start=1):
            for c, col in enumerate(self.columns):
                col_w = col.get("width", 120)
                key = col["key"]
                value = row.get(key, "")

                # 🎨 Soporte de estilo custom para 'estado'
                if key.lower() == "estado":
                    bg_color = row.get("estado_bg")
                    # Fallback si no se dio color específico
                    if not bg_color:
                        val_lower = str(value).lower()
                        if val_lower in ["activo", "disponible", "devuelto en fecha"]:
                            bg_color = "#27ae60"   # verde
                        elif val_lower in ["vencido", "no disponible", "devuelto fuera de término"]:
                            bg_color = "#e74c3c"   # rojo
                        else:
                            bg_color = "#95a5a6"   # gris

                    cell = ctk.CTkFrame(self.body, width=col_w, height=28, fg_color=bg_color, corner_radius=6)
                    cell.grid(row=r, column=c, padx=(0, 10), pady=2, sticky="nsew")
                    lbl = ctk.CTkLabel(cell, text=str(value), text_color="white", anchor="center")
                    lbl.place(relx=0.5, rely=0.5, anchor="center")
                    if self.on_row_click:
                        cell.bind("<Button-1>", lambda e, rr=row: self.on_row_click(rr))
                        lbl.bind("<Button-1>", lambda e, rr=row: self.on_row_click(rr))
                else:
                    lbl = ctk.CTkLabel(self.body, text=str(value), anchor="w", width=col_w)
                    lbl.grid(row=r, column=c, padx=(0, 10), pady=2, sticky="w")
                    if self.on_row_click:
                        lbl.bind("<Button-1>", lambda e, rr=row: self.on_row_click(rr))