import customtkinter as ctk
import os

# Import modular de componentes
from vista.componentes.base_app import BaseApp
from vista.componentes.layout import AppLayout
from vista.componentes.callbacks import get_default_callbacks
from vista.componentes.dashboard_cards import DashboardCards
from vista.componentes.dashboard_stats import DashboardStats


class MainDashboard(BaseApp):
    """Vista principal del panel de control del sistema de biblioteca."""

    def __init__(self, session=None, admin=None):
        super().__init__(title="Biblioteca Pública - Dashboard")

        self.session = session
        self.admin = admin

        callbacks = get_default_callbacks(self)
        banner_path = os.path.join("vista", "images", "banner_bandera.jpg")

        # Layout base
        self.layout = AppLayout(self, banner_image=banner_path, callbacks=callbacks, admin=self.admin)
        self.layout.pack(fill="both", expand=True)

        # Proporciones
        self.layout.main_frame.grid_rowconfigure(0, weight=0)
        self.layout.main_frame.grid_rowconfigure(1, weight=3)
        self.layout.main_frame.grid_rowconfigure(2, weight=2)
        self.layout.main_frame.grid_columnconfigure(0, weight=1)

        # Crear componente de cards
        self._build_cards_component()
        # Crear sección inferior (gráficos)
        self._build_graph_section()

    # ======================================================
    def _build_cards_component(self):
        """Crea el componente de cards y luego las rellena."""
        cards_info = [
            {"titulo": "SOCIOS REGISTRADOS", "pie": "Alta usuario | Editar usuario", "color": "#3498DB", "icon": "people.png"},
            {"titulo": "LIBROS CARGADOS", "pie": "Cargar libro | Editar Libro", "color": "#2ECC71", "icon": "book.png"},
            {"titulo": "PRÉSTAMOS REALIZADOS", "pie": "Nuevo préstamo", "color": "#1ABC9C", "icon": "librarian.png"},
            {"titulo": "PRÉSTAMOS A VENCER", "pie": "Cerrar préstamo", "color": "#E67E22", "icon": "calendar.png"},
        ]

        self.cards_component = DashboardCards(self.layout.main_frame, cards_info=cards_info)
        self.cards_component.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))

        self._rellenar_cards()

    # ======================================================
    def _rellenar_cards(self):
        """Rellena las métricas de las cards y asigna eventos."""
        metricas = {
    "SOCIOS REGISTRADOS": DashboardStats.obtener_total_socios(self.session),
    "LIBROS CARGADOS": DashboardStats.obtener_total_libros(self.session),
    "PRÉSTAMOS REALIZADOS": DashboardStats.obtener_prestamos_emitidos(self.session),
    "PRÉSTAMOS A VENCER": DashboardStats.obtener_prestamos_activos(self.session),
    }


        for titulo, valor in metricas.items():
            card = self.cards_component.get_card_by_title(titulo)
            if card and hasattr(card, "value_label"):
                card.value_label.configure(text=str(valor))

        # Asignar eventos de click a pies
        for card in self.cards_component.winfo_children():
            pie_text = card.footer_label.cget("text").lower()
            if "alta usuario" in pie_text:
                card.footer_label.bind("<Button-1>", lambda e: self._open_new_user())
            elif "editar usuario" in pie_text:
                card.footer_label.bind("<Button-1>", lambda e: self._open_edit_user())
            elif "cargar libro" in pie_text:
                card.footer_label.bind("<Button-1>", lambda e: self._open_new_book())
            elif "editar libro" in pie_text:
                card.footer_label.bind("<Button-1>", lambda e: self._open_edit_book())
            else:
                card.footer_label.bind("<Button-1>", lambda e: self._close_loan())

    # ======================================================
    def _build_graph_section(self):
        """Frame inferior para futuros gráficos."""
        graph_frame = ctk.CTkFrame(self.layout.main_frame, fg_color="#ECF0F1", corner_radius=15)
        graph_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

        lbl = ctk.CTkLabel(graph_frame, text="(Sección de gráficos próximamente)",
                           font=ctk.CTkFont(size=16, weight="bold"),
                           text_color="#2C3E50")
        lbl.pack(pady=20)

    # ======================================================
    # Eventos de navegación
    def _open_new_user(self):
        self.after(100, lambda: self._launch_window("new_user", "NewUser"))
        self.destroy()
        from vista.new_user import NewUser
        NewUser(session=self.session, admin=self.admin)

    def _open_edit_user(self):
        self.after(100, lambda: self._launch_window("edit_user", "EditUser"))
        self.destroy()
        from vista.edit_user import EditUser
        EditUser(session=self.session, admin=self.admin)

    def _open_new_book(self):
        self.after(100, lambda: self._launch_window("new_book", "NewBook"))
        self.destroy()
        from vista.new_book import NewBook
        NewBook(session=self.session, admin=self.admin)

    def _open_edit_book(self):
        self.after(100, lambda: self._launch_window("edit_book", "EditBook"))
        self.destroy()
        from vista.edit_book import EditBook
        EditBook(session=self.session, admin=self.admin)
    
    def _close_loan(self):
        self.after(100, lambda: self._launch_window("loan_active_list", "LoanActiveList"))
        self.destroy()
        from vista.loan_active_list import LoanActiveList
        LoanActiveList(session=self.session, admin=self.admin)


if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()