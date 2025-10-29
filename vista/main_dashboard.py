import customtkinter as ctk
import os
from PIL import Image
from componentes import AppLayout, BaseApp, get_default_callbacks
from dashboard_stats import DashboardStats

class MainDashboard(BaseApp):
    def __init__(self):
        super().__init__(title="Biblioteca Pública - Dashboard")

        callbacks = get_default_callbacks(self)

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
            
            if titulo == 'SOCIOS REGISTRADOS':
                cant_socios = DashboardStats.obtener_total_socios()
                lbl_cantidad = ctk.CTkLabel(card, text=str(cant_socios), text_color="white",font=ctk.CTkFont(size=48, weight="bold"))
                lbl_cantidad.pack(pady=(10, 0))
            elif titulo == 'LIBROS CARGADOS':
                cant_libros = DashboardStats.obtener_total_libros()
                lbl_cantidad = ctk.CTkLabel(card, text=str(cant_libros), text_color="white",font=ctk.CTkFont(size=48, weight="bold"))
                lbl_cantidad.pack(pady=(10, 0))
            elif titulo == 'PRÉSTAMOS REALIZADOS':
                cant_prestamos = DashboardStats.obtener_prestamos_emitidos()
                lbl_cantidad = ctk.CTkLabel(card, text=str(cant_prestamos), text_color="white",font=ctk.CTkFont(size=48, weight="bold"))
                lbl_cantidad.pack(pady=(10, 0))
            else:
                cant_prestamos_vencer = DashboardStats.obtener_prestamos_activos()
                lbl_cantidad = ctk.CTkLabel(card, text=str(cant_prestamos_vencer), text_color="white",font=ctk.CTkFont(size=48, weight="bold"))
                lbl_cantidad.pack(pady=(10, 0))
            
                        
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
                    elif "editar" in texto:
                        link.bind("<Button-1>", lambda e, opt=opcion: self._open_edit_user())
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

        lbl = ctk.CTkLabel(graph_frame, text="Agregar graficos???",font=ctk.CTkFont(size=16, weight="bold"),text_color="#2C3E50")
        lbl.pack(pady=20)
    
    def _open_new_user(self):
        """Abre la vista de alta de usuario."""
        self.destroy()
        from new_user import NewUser
        NewUser()
    
    def _open_edit_user(self):
        """Abre la vista de edición de usuario."""
        self.destroy()
        from edit_user import EditUser
        EditUser()
    
    def _open_new_book(self):
        """Abre la vista de alta de libros."""
        self.destroy()
        from new_book import NewBook
        NewBook()


if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()