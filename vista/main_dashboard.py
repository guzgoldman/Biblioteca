import customtkinter as ctk
import os
from PIL import Image
from componentes import AppLayout, BaseApp, go_to_dashboard, go_to_users, go_to_books, go_to_loans, go_to_exit

class MainDashboard(BaseApp):
    def __init__(self):
        super().__init__(title="Biblioteca Pública - Dashboard")

        callbacks = {
            "Escritorio": lambda: go_to_dashboard(self),
            "Socios": lambda: go_to_users(self),
            "Libros": lambda: go_to_books(self),
            "Préstamos": lambda: go_to_loans(self),
            "Salir": lambda: go_to_exit(self),
        }

        # Estructura base
        self.layout = AppLayout(self, banner_image="vista/images/banner_bandera.jpg", callbacks=callbacks)
        self.layout.pack(fill="both", expand=True)

        # Proporciones del layout general
        self.layout.main_frame.grid_rowconfigure(0, weight=0)  # banner
        self.layout.main_frame.grid_rowconfigure(1, weight=3)  # cards
        self.layout.main_frame.grid_rowconfigure(2, weight=2)  # gráficos
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        self._build_cards()
        self._build_graph_section()

    # ======================================================
    def _build_cards(self):
        """Construye las cards en el main frame."""
        content = ctk.CTkFrame(self.layout.main_frame, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        content.grid_columnconfigure((0, 1), weight=1, uniform="cols")
        content.grid_rowconfigure((0, 1), weight=1, uniform="rows")

        cards_info = [
            ("SOCIOS REGISTRADOS", "Alta usuario | Editar usuario", "#3498DB", "people.png"),
            ("LIBROS CARGADOS", "Cargar libro", "#2ECC71", "book.png"),
            ("PRÉSTAMOS REALIZADOS", "Nuevo préstamo", "#1ABC9C", "librarian.png"),
            ("PRÉSTAMOS A VENCER", "Cerrar préstamo", "#E67E22", "calendar.png"),
        ]

        for idx, (titulo, pie, color, icon_name) in enumerate(cards_info):
            fila, col = divmod(idx, 2)
            card = ctk.CTkFrame(content, fg_color=color, corner_radius=15)
            card.grid(row=fila, column=col, padx=20, pady=20, sticky="nsew")
            card.grid_propagate(False)

            # Tamaño mínimo coherente
            card.configure(width=350, height=180)

            # Ícono
            icon_dir = os.path.join("vista","icons", icon_name)
            icon_img = None
            if os.path.exists(icon_dir):
                img = Image.open(icon_dir).resize((40, 40))
                icon_img = ctk.CTkImage(light_image=img, size=(40, 40))

            row_frame = ctk.CTkFrame(card, fg_color="transparent")
            row_frame.pack(pady=(25, 10))

            if icon_img:
                lbl_icon = ctk.CTkLabel(row_frame, image=icon_img, text="")
                lbl_icon.image = icon_img
                lbl_icon.pack(side="left", padx=(0, 10))

            lbl_titulo = ctk.CTkLabel(row_frame, text=titulo, text_color="white",font=ctk.CTkFont(size=20, weight="bold"))
            lbl_titulo.pack(side="left")
            
            # Footer común
            footer_frame = ctk.CTkFrame(card, fg_color="transparent")
            footer_frame.pack(side="bottom", fill="x", pady=(0, 10))
    
            separator = ctk.CTkFrame(footer_frame, fg_color="#D5D8DC", height=2, corner_radius=0)
            separator.pack(fill="x", padx=20, pady=(0, 6))
    
            # Si hay múltiples opciones en el pie, mostrarlas como enlaces separados
            if "|" in pie:
                opciones = [x.strip() for x in pie.split("|")]
    
                links_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
                links_frame.pack()
    
                for opcion in opciones:
                    link = ctk.CTkLabel(links_frame,
                                        text=opcion,
                                        text_color="white",
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        cursor="hand2")
                    link.pack(side="left", padx=10)
    
                    # Enlace individual con función fija
                    texto = opcion.lower()
                    if "alta" in texto:
                        link.bind("<Button-1>", lambda e, opt=opcion: self._open_new_user())
                        print(link)
                    elif "editar" in texto:
                        link.bind("<Button-1>", lambda e, opt=opcion: self._open_edit_user())
                        print(link)
            else:
                # Pie normal (una sola opción)
                lbl_pie = ctk.CTkLabel(footer_frame, text=pie, text_color="white",
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       cursor="hand2")
                lbl_pie.pack()
    
                if "libro" in pie.lower():
                    lbl_pie.bind("<Button-1>", lambda e: self._open_new_book())


    # ======================================================
    def _build_graph_section(self):
        """Frame inferior para gráficos."""
        graph_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="#ECF0F1", corner_radius=15)
        graph_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

        lbl = ctk.CTkLabel(graph_frame, text="Agregar graficos???",
                           font=ctk.CTkFont(size=16, weight="bold"),
                           text_color="#2C3E50")
        lbl.pack(pady=20)
    
    def _open_new_user(self):
        """Abre la vista de alta de usuario."""
        self.destroy()  # Cierra la ventana actual
        from new_user import NewUser
        NewUser()  # Abre la nueva vista
    
    def _open_edit_user(self):
        """Abre la vista de edición de usuario."""
        self.destroy()  # Cierra la ventana actual
        from edit_user import EditUser
        EditUser()  # Abre la nueva vista
    
    def _open_new_book(self):
        """Abre la vista de alta de libros."""
        self.destroy()  # Cierra la ventana actual
        from new_book import NewBook
        NewBook()  # Abre la nueva vista


if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()