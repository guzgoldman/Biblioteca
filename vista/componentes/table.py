import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import datetime

class Table(ctk.CTkFrame):

    def __init__(self, master, columns, width=1000, height=400, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.columns = columns
        self.width = width
        self.height = height
        self._sorting_state = {}

        # --- Estilos base ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="white",
            foreground="#2c3e50",
            rowheight=32,
            fieldbackground="white",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Treeview.Heading",
            background="#ecf0f1",
            foreground="#2c3e50",
            font=("Segoe UI", 11, "bold"),
        )
        style.map(
            "Treeview",
            background=[
                ("selected", "#d6eaf8")  # ✅ Azul suave visible
            ],
            foreground=[
                ("selected", "#000000")  # Texto negro sobre el azul
            ],
        )

        # --- Treeview ---
        self.tree = ttk.Treeview(
            self,
            columns=[col["key"] for col in self.columns],
            show="headings",
            height=int(height / 30),
        )
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Encabezados y anchos
        for col in self.columns:
            self.tree.heading(col["key"], text=col["text"],command=lambda c=col["key"]: self._sort_by_column(c))
            self.tree.column(col["key"], width=col.get("width", 120), anchor="center")

        # Tags de colores (verde y rojo)
        self.tree.tag_configure("due_green", foreground="#27ae60")
        self.tree.tag_configure("due_red", foreground="#e74c3c")

    # =====================================================
    def clear(self):
        """Elimina todas las filas."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    # =====================================================
    def set_data(self, data):
        """
        Carga datos en la tabla.
        Cada fila es un dict con keys que coincidan con self.columns.
        """
        self.clear()
        for row in data:
            tags = row.get("_tags", ())
            values = [row.get(col["key"], "") for col in self.columns]
            self.tree.insert("", "end", values=values, tags=tags)

    # =====================================================
    def bind_cell_click(self, handler):
        """
        Permite capturar clics en celdas específicas.
        El handler recibe (row_id, col_key).
        """
        def on_click(event):
            region = self.tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            row_id = self.tree.identify_row(event.y)
            col_id = self.tree.identify_column(event.x)
            if not row_id or not col_id:
                return
            col_index = int(col_id.replace("#", "")) - 1
            col_key = self.columns[col_index]["key"]
            handler(row_id, col_key)

        self.tree.bind("<ButtonRelease-1>", on_click)

    # =====================================================
    
        # =====================================================
    def _sort_by_column(self, col_key):
        """Ordena la tabla por una columna (ASC/DESC alternado, soporta fechas dd/mm/yyyy)."""

        import re
        from datetime import datetime

        try:
            col_index = next(i for i, c in enumerate(self.columns) if c["key"] == col_key)
        except StopIteration:
            return

        rows = list(self.tree.get_children())

        if not rows:
            return

        sample = None
        for row_id in rows:
            vals = self.tree.item(row_id)["values"]
            if col_index < len(vals):
                v = vals[col_index]
                s = str(v).strip()
                if s:
                    sample = s
                    break

        if sample is None:
            return

        is_date_col = bool(re.match(r"^\d{2}/\d{2}/\d{4}$", sample))
        is_numeric_col = False
        if not is_date_col:
            try:
                float(sample.replace(",", "."))
                is_numeric_col = True
            except ValueError:
                is_numeric_col = False

        reverse = self._sorting_state.get(col_key, False)
        self._sorting_state[col_key] = not reverse

        def parse_value(v):
            s = str(v).strip()
            if s == "":
                return (1, None)

            if is_date_col:
                try:
                    dt = datetime.strptime(s, "%d/%m/%Y")
                    return (0, dt)
                except ValueError:
                    return (0, s.lower())

            if is_numeric_col:
                try:
                    num = float(s.replace(",", "."))
                    return (0, num)
                except ValueError:
                    return (0, s.lower())

            return (0, s.lower())

        data = []
        for row_id in rows:
            vals = self.tree.item(row_id)["values"]
            value = vals[col_index] if col_index < len(vals) else ""
            data.append((parse_value(value), row_id))

        # Ordenar
        data.sort(key=lambda x: x[0], reverse=reverse)

        for index, (_, row_id) in enumerate(data):
            self.tree.move(row_id, "", index)

        for col in self.columns:
            self.tree.heading(col["key"], text=col["text"])

        # Agregar flecha a la columna ordenada
        arrow = " ▲" if not reverse else " ▼"
        header_text = next(c["text"] for c in self.columns if c["key"] == col_key)
        self.tree.heading(col_key, text=header_text + arrow)
