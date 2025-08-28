import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# LOGIN
def validar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if not usuario or not contrasena:
        messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
        return
    try:
        conn = sqlite3.connect('Usuarios')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Email = ? AND Contraseña = ? AND IFNULL(esAdministrador,0) = 1', (usuario, contrasena))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            root.destroy()  # Cerrar ventana de login
            import graphic_interface  # Importar el módulo CRUD después del login exitoso
            graphic_interface.main()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

def set_db():
    try:
        conn = sqlite3.connect('Usuarios')
        cursor = conn.cursor()
        cursor.execute('''
            DROP TABLE IF EXISTS Usuarios;
        ''')
        conn.commit()
        cursor.execute('''
            CREATE TABLE Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Email VARCHAR(30) NOT NULL,
                Inactivo TINYINT NOT NULL DEFAULT 0,
                Contraseña VARCHAR(50) NOT NULL,
                UltimaConexion DATETIME DEFAULT CURRENT_TIMESTAMP,
                esAdministrador BOOLEAN DEFAULT FALSE
            )
        ''')
        conn.commit()
        cursor.execute('''
            INSERT INTO Usuarios (Email, Contraseña,esAdministrador)
            VALUES ('admin@admin.com', '1234',True)
        ''')
        conn.commit()
        conn.close()
        messagebox.showinfo("Conexión", "Base de datos conectada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")


# VENTANA PRINCIPAL
root = tk.Tk()
root.title("Login de Aplicación")
root.state('zoomed')  # Pantalla completa en Windows (en Linux/Mac: root.attributes('-fullscreen', True))
set_db()

# Frame centrado
frame_login = ttk.Frame(root, padding=30, relief="raised")
frame_login.place(relx=0.5, rely=0.5, anchor="center")

# Etiqueta de título
label_titulo = ttk.Label(frame_login, text="Iniciar Sesión", font=("Segoe UI", 16, "bold"))
label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Usuario
label_usuario = ttk.Label(frame_login, text="Usuario:")
label_usuario.grid(row=1, column=0, sticky="e", padx=5, pady=5)

entry_usuario = ttk.Entry(frame_login, width=30)
entry_usuario.grid(row=1, column=1, pady=5)

# Contraseña
label_contrasena = ttk.Label(frame_login, text="Contraseña:")
label_contrasena.grid(row=2, column=0, sticky="e", padx=5, pady=5)

entry_contrasena = ttk.Entry(frame_login, show="*", width=30)
entry_contrasena.grid(row=2, column=1, pady=5)

# Botón login
btn_login = ttk.Button(frame_login, text="Ingresar", command=validar_login)
btn_login.grid(row=3, column=0, columnspan=2, pady=(15, 0))

# Foco inicial en el campo usuario
entry_usuario.focus()

root.mainloop()