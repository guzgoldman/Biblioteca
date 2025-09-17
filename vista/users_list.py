import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import customtkinter as ctk
from PIL import Image
from sqlalchemy.orm import Session
from db.Conector import SessionLocal
from modelo.Socio import Socio

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class UserList(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Listado de Socios")
        self.geometry("1000x600")

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
                btn = ctk.CTkButton(self.sidebar, text=text, width=160, anchor="w", image=self.icons[icon], compound="left")
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

        # Resize dinámico
        def update_images(event=None):
            width = self.main_frame.winfo_width()
            height = self.main_frame.winfo_height()

            # Banner fijo en 150px de alto
            banner_img = ctk.CTkImage(light_image=self.banner_original, size=(width, 150))
            self.banner_label.configure(image=banner_img)
            self.banner_label.image = banner_img

            # Fondo rellena debajo del banner
            #bg_height = max(height - 150, 200)
            #bg_img = ctk.CTkImage(light_image=self.bg_original, size=(width, bg_height))
            #self.bg_label.configure(image=bg_img)
            #self.bg_label.image = bg_img

        self.main_frame.bind("<Configure>", update_images)
        
        self.socios_frame = ctk.CTkScrollableFrame(self.main_frame, width=700, height=350)
        self.socios_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=20)

        self.cargar_socios()

    def cargar_socios(self):
        # Encabezados
        headers = ["DNI", "Nombre", "Apellido", "Dirección"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.socios_frame, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky="w")
        # Cargar datos de la base
        session: Session = SessionLocal()
        socios = session.query(Socio).all()
        for row, socio in enumerate(socios, start=1):
            ctk.CTkLabel(self.socios_frame, text=socio.dni).grid(row=row, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.socios_frame, text=socio.nombre).grid(row=row, column=1, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.socios_frame, text=socio.apellido).grid(row=row, column=2, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(self.socios_frame, text=getattr(socio, "direccion", "")).grid(row=row, column=3, padx=10, pady=2, sticky="w")
        session.close()

def main():
    app = UserList()
    app.mainloop()

if __name__ == "__main__":
    main()