import customtkinter as ctk
from PIL import Image

# Configuración inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Biblioteca")
        self.geometry("1000x600")

        # === ICONOS ===
        self.icons = {
            "home": ctk.CTkImage(light_image=Image.open("vista/icons/home.png"), size=(20, 20)),
            "user": ctk.CTkImage(light_image=Image.open("vista/icons/user.png"), size=(20, 20)),
            "book": ctk.CTkImage(light_image=Image.open("vista/icons/book.png"), size=(20, 20)),
            "send": ctk.CTkImage(light_image=Image.open("vista/icons/send.png"), size=(20, 20)),
            "check": ctk.CTkImage(light_image=Image.open("vista/icons/check.png"), size=(20, 20)),
            "cancel": ctk.CTkImage(light_image=Image.open("vista/icons/cancel.png"), size=(20, 20)),
            "calendar": ctk.CTkImage(light_image=Image.open("vista/icons/calendar.png"), size=(20, 20)),
            "logout": ctk.CTkImage(light_image=Image.open("vista/icons/logout.png"), size=(20, 20)),
        }

        # === SIDEBAR ===
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Menú", 
                                          font=ctk.CTkFont(size=18, weight="bold"))
        self.sidebar_label.pack(pady=(20, 10))

        menu_items = [
            ("Escritorio", "home"),
            ("Socios", "user"),
            ("Libros", "book"),
            ("Emitidos", "send"),
            ("Devueltos", "check"),
            ("No Devueltos", "cancel"),
            ("Salir", "logout")
        ]

        for text, icon in menu_items:
            if  text == "Socios":
                btn = ctk.CTkButton(self.sidebar, text=text, width=160, anchor="w", image=self.icons[icon], compound="left",command=self.open_socios_window)
            else:
                btn = ctk.CTkButton(self.sidebar, text=text, width=160, anchor="w", image=self.icons[icon], compound="left")
            btn.pack(pady=5, padx=10)

        # === MAIN CONTENT ===
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.main_frame.grid_columnconfigure((0,1,2), weight=1, minsize=160)
        self.main_frame.grid_rowconfigure(0, weight=0)  # Banner
        self.main_frame.grid_rowconfigure(1, weight=0, minsize=160)
        self.main_frame.grid_rowconfigure(2, weight=0, minsize=160)

        self.banner_original = Image.open("vista/images/banner_bandera.jpg")
        self.bg_original = Image.open("vista/images/biblioteca.jpg")

        # Banner
        banner_img = ctk.CTkImage(light_image=self.banner_original, size=(self.winfo_width(), 150))
        self.banner_label = ctk.CTkLabel(
            self.main_frame,
            text="Biblioteca Central de Buenos Aires - Panel de Control",
            image=banner_img,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="black",
            compound="center"
        )
        self.banner_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.banner_label.image = banner_img

        # Fondo
        bg_img = ctk.CTkImage(light_image=self.bg_original, size=(self.winfo_width(), 200))
        self.bg_label = ctk.CTkLabel(self.main_frame, text="", image=bg_img)
        self.bg_label.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="nsew")
        self.bg_label.image = bg_img

        # Resize dinámico
        def update_images(event=None):
            width = self.main_frame.winfo_width()
            height = self.main_frame.winfo_height()

            # Banner fijo en 150px de alto
            banner_img = ctk.CTkImage(light_image=self.banner_original, size=(width, 150))
            self.banner_label.configure(image=banner_img)
            self.banner_label.image = banner_img

            # Fondo rellena debajo del banner
            bg_height = max(height - 150, 200)
            bg_img = ctk.CTkImage(light_image=self.bg_original, size=(width, bg_height))
            self.bg_label.configure(image=bg_img)
            self.bg_label.image = bg_img

        self.main_frame.bind("<Configure>", update_images)


        # === CARDS ===
        self.create_card("3\nLibros", "book", "#3498db", 1, 0)
        self.create_card("2\nSocios", "user", "#2ecc71", 1, 1)
        self.create_card("Emitidos: 2", "send", "#2980b9", 1, 2)

        self.create_card("Devueltos: 1", "check", "#27ae60", 2, 0)
        self.create_card("No Devueltos: 1", "cancel", "#16a085", 2, 1)
        self.create_card("Fecha: 03/04/2018", "calendar", "#d35400", 2, 2)

    def create_card(self, text, icon, color, row, col):
        frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=color, width=160, height=120)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="n")
        frame.lift() 

        label_icon = ctk.CTkLabel(frame, image=self.icons[icon], text="")
        label_icon.place(relx=0.1, rely=0.2, anchor="w")

        label_text = ctk.CTkLabel(frame, text=text, text_color="white",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        label_text.place(relx=0.5, rely=0.6, anchor="center")
    
    def open_socios_window(self):
        self.destroy()
        import users_list  # Importar el módulo CRUD después del login exitoso
        users_list.main()

def main():
    app = DashboardApp()
    app.mainloop()

if __name__ == "__main__":
    main()