# main_dashboard.py
import customtkinter as ctk
from componenentes import BaseWindow, Sidebar, default_menu

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

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="n", pady=20)
        for col in range(3):
            self.content_frame.grid_columnconfigure(col, weight=1)

        self.create_card("3\nLibros", "book", "#3498db", 0, 0)
        self.create_card("2\nSocios", "user", "#2ecc71", 0, 1)
        self.create_card("Emitidos: 2", "send", "#2980b9", 0, 2)
        self.create_card("Devueltos: 1", "check", "#27ae60", 1, 0)
        self.create_card("No Devueltos: 1", "cancel", "#16a085", 1, 1)
        self.create_card("Fecha: 03/04/2018", "calendar", "#d35400", 1, 2)
    
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