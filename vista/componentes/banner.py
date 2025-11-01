import customtkinter as ctk
from PIL import Image, ImageOps
import os

class Banner(ctk.CTkFrame):
    """Banner superior redimensionable."""
    def __init__(self, master, image_path=None, fixed_height=250, **kwargs):
        super().__init__(master, fg_color="white", height=fixed_height, corner_radius=0, **kwargs)
        self.grid_propagate(False)
        self.fixed_height = fixed_height
        self.label = ctk.CTkLabel(self, text="", fg_color="white")
        self.label.pack(fill="both", expand=True)

        self._banner_img_original = None
        self._last_width = 0
        if image_path and os.path.exists(image_path):
            self._banner_img_original = Image.open(image_path).convert("RGB")

        self.after(100, self._initial_draw)

    def _initial_draw(self):
        if not self._banner_img_original:
            self.configure(fg_color="#2C3E50")
            return

        if self.winfo_width() < 50:
            self.after(100, self._initial_draw)
            return

        self._redraw_banner()
        if self.master:
            self.master.bind("<Configure>", self._on_resize, add="+")

    def _on_resize(self, event=None):
        new_width = self.winfo_width()
        if abs(new_width - self._last_width) > 10:
            self._redraw_banner()

    def _redraw_banner(self):
        if not self._banner_img_original:
            return
        width = max(50, self.winfo_width())
        height = self.fixed_height
        img = ImageOps.fit(self._banner_img_original, (width, height))
        tkimg = ctk.CTkImage(light_image=img, size=(width, height))
        self.label.configure(image=tkimg)
        self.label.image = tkimg
        self._last_width = width