import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class Table(ctk.CTkFrame):
    """
    Tabla reutilizable basada en ttk.Treeview.
    Soporta:
      - Texto coloreado (usando tags)
      - Botones simulados (clics en columnas específicas)
    """

    def __init__(self, master, columns, width=1000, height=400, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.columns = columns
        self.width = width
        self.height = height

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
            self.tree.heading(col["key"], text=col["text"])
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
    def tag_config(self):
        """Compatibilidad (no hace falta, ya configurado arriba)."""
        pass