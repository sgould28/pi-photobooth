
import tkinter as tk
import threading
from PIL import Image, ImageTk

from camera import take_photo


class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photo Booth")

        # Fullscreen 800x480 touchscreen
        self.root.geometry("800x480")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#181827")

        self.root.bind(
            "<Escape>",
            lambda event: self.root.destroy()
        )

        self.image_ref = None
        self.photo_path = None

        self.show_home()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_label(self, parent, text, size=24):
        return tk.Label(
            parent,
            text=text,
            font=("Arial", size, "bold"),
            fg="white",
            bg="#181827"
        )

    def make_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 15, "bold"),
            bg="#e89ab0",
            fg="#181827",
            activebackground="#f4b6ca",
            padx=12,
            pady=6,
            relief="flat"
        )

    def make_page(self):
        self.clear_screen()

        page = tk.Frame(
            self.root,
            bg="#181827",
            width=800,
            height=480
        )
        page.pack(fill="both", expand=True)
        page.pack_propagate(False)

        return page

    def add_exit(self, page):
        self.make_button(
            page,
            "EXIT",
            self.root.destroy
        ).place(x=680, y=12, width=105, height=42)

    def show_home(self):
        page = self.make_page()
        self.add_exit(page)

        self.make_label(
            page, "MINI PHOTO BOOTH", 30
        ).place(x=120, y=90, width=560, height=70)

        self.make_button(
            page, "TAKE PHOTO",
            lambda: self.countdown(3)
        ).place(x=260, y=215, width=280, height=70)

        self.make_label(
            page, "Tap to capture a memory!", 15
        ).place(x=180, y=320, width=440, height=45)

    def countdown(self, number):
        page = self.make_page()
        self.add_exit(page)

        self.make_label(
            page, "GET READY!", 28
        ).place(x=200, y=65, width=400, height=60)

        self.make_label(
            page, str(number), 85
        ).place(x=300, y=145, width=200, height=170)

        if number > 0:
            self.root.after(
                1000,
                lambda: self.countdown(number - 1)
            )
        else:
            self.capture()

    def capture(self):
        page = self.make_page()
        self.add_exit(page)

        self.make_label(
            page, "Taking your photo...", 24
        ).place(x=150, y=175, width=500, height=75)

        threading.Thread(
            target=self.capture_worker,
            daemon=True
        ).start()

    def capture_worker(self):
        try:
            path = take_photo()

            self.root.after(
                0,
                lambda: self.show_photo(path)
            )

        except Exception as error:
            message = str(error)

            self.root.after(
                0,
                lambda: self.show_error(message)
            )

    def show_photo(self, path):
        self.photo_path = path
        page = self.make_page()
        self.add_exit(page)

        self.make_label(
            page, "YOUR PHOTO!", 25
        ).place(x=210, y=5, width=380, height=50)

        with Image.open(path) as original:
            image = original.copy()

        image.thumbnail((570, 325))
        self.image_ref = ImageTk.PhotoImage(image)

        photo_label = tk.Label(
            page,
            image=self.image_ref,
            bg="#181827"
        )
        photo_label.place(
            x=400 - image.width // 2,
            y=60,
            width=image.width,
            height=image.height
        )

        self.make_button(
            page, "TAKE ANOTHER",
            self.show_home
        ).place(x=280, y=400, width=240, height=55)

    def show_error(self, message):
        page = self.make_page()
        self.add_exit(page)

        self.make_label(
            page, "Camera Error", 25
        ).place(x=200, y=60, width=400, height=60)

        tk.Label(
            page,
            text=message[-350:],
            font=("Arial", 12),
            fg="white",
            bg="#181827",
            wraplength=650,
            justify="center"
        ).place(x=75, y=140, width=650, height=175)

        self.make_button(
            page, "BACK",
            self.show_home
        ).place(x=300, y=365, width=200, height=55)
