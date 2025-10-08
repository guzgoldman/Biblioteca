import sys
from pathlib import Path

# Agregar el directorio padre al path para poder importar los módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class LoginWindow(ctk.CTk):
    """Ventana de login para administradores del sistema de biblioteca."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Biblioteca - Login")
        self.geometry("500x400")
        
        # Centrar ventana
        self.center_window()
        
        # Variable para guardar el administrador autenticado
        self.admin_autenticado = None
        
        # Configurar UI
        self.crear_interfaz()
        
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = 500
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz del login."""
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        titulo_label = ctk.CTkLabel(
            main_frame,
            text="🔐 Sistema de Biblioteca",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2c3e50"
        )
        titulo_label.pack(pady=(30, 10))
        
        subtitulo_label = ctk.CTkLabel(
            main_frame,
            text="Acceso para Administradores",
            font=ctk.CTkFont(size=14),
            text_color="#7f8c8d"
        )
        subtitulo_label.pack(pady=(0, 30))
        
        # Frame para campos de entrada
        campos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        campos_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Campo DNI
        dni_label = ctk.CTkLabel(
            campos_frame,
            text="DNI:",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        dni_label.pack(pady=(0, 5), anchor="w")
        
        self.entry_dni = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Ingrese su DNI",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.entry_dni.pack(fill="x", pady=(0, 15))
        
        # Campo Contraseña
        password_label = ctk.CTkLabel(
            campos_frame,
            text="Contraseña:",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        password_label.pack(pady=(0, 5), anchor="w")
        
        self.entry_password = ctk.CTkEntry(
            campos_frame,
            placeholder_text="Ingrese su contraseña",
            show="•",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.entry_password.pack(fill="x", pady=(0, 20))
        
        # Botón de login
        self.btn_login = ctk.CTkButton(
            campos_frame,
            text="Iniciar Sesión",
            command=self.validar_login,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_login.pack(fill="x", pady=(10, 0))
        
        # Bind Enter key
        self.entry_dni.bind("<Return>", lambda e: self.entry_password.focus())
        self.entry_password.bind("<Return>", lambda e: self.validar_login())
        
        # Foco inicial
        self.entry_dni.focus()
    
    def validar_login(self):
        """Valida las credenciales del administrador."""
        dni = self.entry_dni.get().strip()
        password = self.entry_password.get().strip()
        
        # Validar campos vacíos
        if not dni or not password:
            messagebox.showwarning(
                "Campos Vacíos",
                "Por favor, complete todos los campos."
            )
            return
        
        # Deshabilitar botón mientras se valida
        self.btn_login.configure(state="disabled", text="Validando...")
        self.update()
        
        try:
            # Importar módulos de base de datos
            from db.Conector import SessionLocal
            from modelo.Administrador import Administrador
            
            # Crear sesión
            session = SessionLocal()
            
            try:
                # Buscar administrador por DNI
                admin = session.query(Administrador).filter_by(dni=dni).first()
                
                print(f"Administrador encontrado: {admin}")
                if admin:
                    print(f"Nombre: {admin.nombre}, Apellido: {admin.apellido}")
                
                if admin and admin.verificar_password(password):
                    # Login exitoso
                    self.admin_autenticado = admin
                    messagebox.showinfo(
                        "Éxito",
                        f"¡Bienvenido, {admin.nombre} {admin.apellido}!"
                    )
                    
                    # Cerrar login y abrir dashboard
                    self.abrir_dashboard()
                else:
                    # Credenciales incorrectas
                    messagebox.showerror(
                        "Error de Autenticación",
                        "DNI o contraseña incorrectos."
                    )
                    self.entry_password.delete(0, 'end')
                    self.entry_password.focus()
                    
            finally:
                session.close()
                
        except Exception as e:
            messagebox.showerror(
                "Error de Conexión",
                f"No se pudo conectar con la base de datos.\n\nError: {str(e)}"
            )
            print(f"Error en login: {e}")
        
        finally:
            # Rehabilitar botón
            self.btn_login.configure(state="normal", text="Iniciar Sesión")
    
    def abrir_dashboard(self):
        """Cierra el login y abre el dashboard principal."""
        self.destroy()
        
        # Importar y abrir dashboard
        from main_dashboard import mainDashBoard
        app = mainDashBoard()
        
        # Guardar referencia al admin autenticado
        app.admin_autenticado = self.admin_autenticado
        app.mainloop()


def main():
    """Función principal para ejecutar el login."""
    app = LoginWindow()
    app.mainloop()


if __name__ == "__main__":
    main()