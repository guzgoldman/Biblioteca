import sys
from pathlib import Path
from tkinter import messagebox
import customtkinter as ctk

# Asegurar importaciones desde el proyecto raíz
sys.path.insert(0, str(Path(__file__).parent.parent))

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):
    """Ventana de login para administradores del sistema de biblioteca."""

    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Biblioteca - Login")
        self.geometry("500x400")
        self.resizable(False, False)
        self.center_window()

        # Variables
        self.admin_autenticado = None
        self.session_activa = None

        # Crear interfaz
        self.crear_interfaz()

    # =====================================================
    def center_window(self):
        """Centra la ventana en pantalla."""
        self.update_idletasks()
        width, height = 500, 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # =====================================================
    def crear_interfaz(self):
        """Crea la interfaz del login usando grid layout."""
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Configurar grillas
        main_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # ----------- Título y subtítulo -----------
        titulo_label = ctk.CTkLabel(
            main_frame,
            text="🔐 Sistema de Biblioteca",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#2c3e50"
        )
        titulo_label.grid(row=0, column=0, pady=(10, 0), sticky="n")

        subtitulo_label = ctk.CTkLabel(
            main_frame,
            text="Acceso para Administradores",
            font=ctk.CTkFont(size=13),
            text_color="#7f8c8d"
        )
        subtitulo_label.grid(row=1, column=0, pady=(0, 10))

        # ----------- Frame de campos -----------
        campos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.grid(row=2, column=0, pady=(0, 5), padx=40, sticky="n")
        campos_frame.grid_columnconfigure(0, weight=1)

        entry_width = 320

        # DNI
        dni_label = ctk.CTkLabel(
            campos_frame, text="DNI:", font=ctk.CTkFont(size=13), anchor="w"
        )
        dni_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_dni = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Ingrese su DNI",
            height=40,
            width=entry_width,
            font=ctk.CTkFont(size=13)
        )
        self.entry_dni.grid(row=1, column=0, pady=(0, 15))

        # Contraseña
        password_label = ctk.CTkLabel(
            campos_frame, text="Contraseña:", font=ctk.CTkFont(size=13), anchor="w"
        )
        password_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.entry_password = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Ingrese su contraseña",
            show="•",
            height=40,
            width=entry_width,
            font=ctk.CTkFont(size=13)
        )
        self.entry_password.grid(row=3, column=0, pady=(0, 10))

        # ----------- Botón Login -----------
        self.btn_login = ctk.CTkButton(
            main_frame,
            text="Iniciar Sesión",
            command=self.validar_login,
            height=42,
            width=entry_width,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_login.grid(row=3, column=0, pady=(10, 10))

        # Bind tecla Enter
        self.entry_dni.bind("<Return>", lambda e: self.entry_password.focus())
        self.entry_password.bind("<Return>", lambda e: self.validar_login())

        # Foco inicial
        self.entry_dni.focus()

    # =====================================================
    def validar_login(self):
        """Valida las credenciales del administrador."""
        dni = self.entry_dni.get().strip()
        password = self.entry_password.get().strip()

        if not dni or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        self.btn_login.configure(state="disabled", text="Validando...")
        self.update()

        try:
            from db.Conector import SessionLocal
            from modelo.Administrador import Administrador

            session = SessionLocal()

            admin = session.query(Administrador).filter_by(dni=dni).first()
            print(f"Administrador encontrado: {admin}")

            if admin and admin.verificar_password(password):
                self.admin_autenticado = admin
                self.session_activa = session
                messagebox.showinfo("Éxito", f"¡Bienvenido, {admin.nombre} {admin.apellido}!")
                self.abrir_dashboard()
                return
            else:
                messagebox.showerror("Error de Autenticación", "DNI o contraseña incorrectos.")
                self.entry_password.delete(0, 'end')
                self.entry_password.focus()

        except Exception as e:
            messagebox.showerror(
                "Error de Conexión",
                f"No se pudo conectar con la base de datos.\n\nError: {str(e)}"
            )
            print(f"Error en login: {e}")
        finally:
            try:
                if self.winfo_exists():
                    self.btn_login.configure(state="normal", text="Iniciar Sesión")
            except:
                pass

    # =====================================================
    def abrir_dashboard(self):
        """Cierra el login y abre el dashboard principal."""
        self.destroy()
        from vista.main_dashboard import MainDashboard
        app = MainDashboard(session=self.session_activa, admin=self.admin_autenticado)
        app.mainloop()


# =====================================================
def main():
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()