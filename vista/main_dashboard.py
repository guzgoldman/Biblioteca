# main_dashboard.py
import customtkinter as ctk
from componenentes import BaseWindow, Sidebar, default_menu
from dashboard_stats import DashboardStats

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class mainDashBoard(BaseWindow):
    def __init__(self):
        super().__init__(title="Biblioteca - Panel Principal")

        actions = {
            "Escritorio": self.go_dashboard,
            "Socios": self.go_socios,
            "Libros": self.go_books,
            "Préstamos": self.toggle_prestamos,
            "Salir": self.quit
        }
        # Submenú para Préstamos
        submenus = {
            "Préstamos": [
                ("Activos", self.go_prestamos_activos),
                ("Historial", self.go_prestamos_historial)
            ]
        }
        self.build_sidebar_with_submenus(actions, submenus)

        # Cargar estadísticas desde la base de datos
        self.cargar_estadisticas()

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=20)
        for col in range(3):
            self.content_frame.grid_columnconfigure(col, weight=1)

        # Crear tarjetas con datos reales
        self.create_card(
            f"{self.stats['total_libros']}\nLibros", 
            "book", 
            "#3498db", 
            0, 0
        )
        self.create_card(
            f"{self.stats['total_socios']}\nSocios", 
            "user", 
            "#2ecc71", 
            0, 1
        )
        self.create_card(
            f"Emitidos: {self.stats['prestamos_emitidos']}", 
            "send", 
            "#2980b9", 
            0, 2
        )
        self.create_card(
            f"Devueltos: {self.stats['prestamos_devueltos']}", 
            "check", 
            "#27ae60", 
            1, 0
        )
        self.create_card(
            f"Activos: {self.stats['prestamos_activos']}", 
            "cancel", 
            "#16a085", 
            1, 1
        )
        self.create_card(
            f"Fecha: {self.stats['fecha_actual']}", 
            "calendar", 
            "#d35400", 
            1, 2
        )
        
        # Agregar sección de estadísticas adicionales
        self.crear_seccion_estadisticas_detalladas()
    
    def crear_seccion_estadisticas_detalladas(self):
        """Crea una sección con estadísticas más detalladas."""
        stats_detail_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#ecf0f1")
        stats_detail_frame.grid(row=2, column=0, sticky="ew", pady=20, padx=40)
        
        # Título de la sección
        title_label = ctk.CTkLabel(
            stats_detail_frame, 
            text="📊 Estadísticas Detalladas del Sistema", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2c3e50"
        )
        title_label.pack(pady=(15, 10))
        
        # Frame para las estadísticas
        stats_info_frame = ctk.CTkFrame(stats_detail_frame, fg_color="transparent")
        stats_info_frame.pack(pady=10, padx=20, fill="both")
        
        # Configurar columnas
        stats_info_frame.grid_columnconfigure(0, weight=1)
        stats_info_frame.grid_columnconfigure(1, weight=1)
        
        # Información de libros y ejemplares
        libros_info = f"📚 Total de Libros: {self.stats['total_libros']} | Ejemplares: {self.stats['total_ejemplares']}"
        libros_label = ctk.CTkLabel(
            stats_info_frame, 
            text=libros_info, 
            font=ctk.CTkFont(size=13),
            text_color="#34495e"
        )
        libros_label.grid(row=0, column=0, sticky="w", pady=5, padx=10)
        
        # Información de socios
        socios_info = f"👥 Total de Socios: {self.stats['total_socios']}"
        socios_label = ctk.CTkLabel(
            stats_info_frame, 
            text=socios_info, 
            font=ctk.CTkFont(size=13),
            text_color="#34495e"
        )
        socios_label.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        
        # Información de préstamos
        prestamos_info = f"📤 Préstamos Totales: {self.stats['prestamos_emitidos']} | Activos: {self.stats['prestamos_activos']} | Devueltos: {self.stats['prestamos_devueltos']}"
        prestamos_label = ctk.CTkLabel(
            stats_info_frame, 
            text=prestamos_info, 
            font=ctk.CTkFont(size=13),
            text_color="#34495e"
        )
        prestamos_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5, padx=10)
        
        # Alerta de préstamos vencidos (si hay)
        if self.stats['prestamos_vencidos'] > 0:
            vencidos_info = f"⚠️ ATENCIÓN: {self.stats['prestamos_vencidos']} préstamos vencidos"
            vencidos_label = ctk.CTkLabel(
                stats_info_frame, 
                text=vencidos_info, 
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#e74c3c"
            )
            vencidos_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=5, padx=10)
        
        # Botón de actualizar
        refresh_btn = ctk.CTkButton(
            stats_detail_frame,
            text="🔄 Actualizar Estadísticas",
            command=self.actualizar_dashboard,
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=8,
            height=35
        )
        refresh_btn.pack(pady=(10, 15))
    
    def cargar_estadisticas(self):
        """Carga las estadísticas desde la base de datos."""
        try:
            self.stats = DashboardStats.obtener_todas_estadisticas()
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")
            # Valores por defecto en caso de error
            self.stats = {
                'total_libros': 0,
                'total_ejemplares': 0,
                'total_socios': 0,
                'prestamos_emitidos': 0,
                'prestamos_activos': 0,
                'prestamos_devueltos': 0,
                'prestamos_vencidos': 0,
                'fecha_actual': DashboardStats.obtener_fecha_actual()
            }
    
    def actualizar_dashboard(self):
        """Actualiza el dashboard recargando la ventana con datos frescos."""
        self.destroy()
        mainDashBoard().mainloop()
    
    def build_sidebar_with_submenus(self, actions, submenus):
        # helper usando Sidebar mejorado (ver cambios en componenentes.py abajo)
        self.sidebar = None
        self.sidebar = Sidebar(self.container, self.icons, default_menu(actions), actions=actions, submenus=submenus)
        self.sidebar.grid(row=0, column=0, sticky="ns")

    def create_card(self, text, icon, color, row, col):
        frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color=color, width=160, height=120)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        if self.icons.get(icon):
            ctk.CTkLabel(frame, image=self.icons[icon], text="").place(relx=0.1, rely=0.2, anchor="w")
        ctk.CTkLabel(frame, text=text, text_color="white", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.6, anchor="center")

    # Navegación
    def go_dashboard(self):
        self.destroy()
        mainDashBoard().mainloop()

    def go_socios(self):
        from users_list import UserList
        self.destroy()
        UserList().mainloop()

    def go_books(self):
        from books_list import BookList
        self.destroy()
        BookList().mainloop()

    def go_prestamos_activos(self):
        from loan_active_list import LoanActiveList
        self.destroy()
        LoanActiveList().mainloop()

    def go_prestamos_historial(self):
        from loan_history_list import LoanHistoryList
        self.destroy()
        LoanHistoryList().mainloop()

    def toggle_prestamos(self):
        # El Sidebar maneja el despliegue; este método es sólo placeholder para 'Préstamos'
        pass

def main():
    app = mainDashBoard()
    app.mainloop()

if __name__ == "__main__":
    main()