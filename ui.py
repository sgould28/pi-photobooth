
import tkinter as tk
import threading
from PIL import Image, ImageTk

from camera import take_photo


class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photo Booth")
        self.root.geometry("800x480")
        self.root.configure(bg="#181827")

        self.image_ref = None
        self.photo_path = None

        self.show_home()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_label(self, text, size=28):
        return tk.Label(
            self.root,
            text=text,
            font=("Arial", size, "bold"),
            fg="white",
            bg="#181827"
        )

    def make_button(self, text, command):
        return tk.Button(
            self.root,
            text=text,
            command=command,
            font=("Arial", 20, "bold"),
            bg="#e89ab0",
            fg="#181827",
            padx=20,
            pady=10
        )

    def show_home(self):
        self.clear_screen()

        self.make_label("MINI PHOTO BOOTH", 36).pack(pady=75)

        self.make_button(
            "TAKE PHOTO",
            lambda: self.countdown(3)
        ).pack(pady=20)

    def countdown(self, number):
        self.clear_screen()

        if number > 0:
            self.make_label("GET READY!", 28).pack(pady=50)
            self.make_label(str(number), 90).pack(pady=10)

            self.root.after(
                1000,
                lambda: self.countdown(number - 1)
            )
        else:
            self.capture()

    def capture(self):
        self.clear_screen()
        self.make_label("Taking your photo...", 28).pack(pady=150)

        threading.Thread(
            target=self.capture_worker,
            daemon=True
        ).start()

    def capture_worker(self):
        try:
            path = take_photo()
            self.root.after(0, lambda: self.show_photo(path))
        except Exception as error:
            message = str(error)
            self.root.after(0, lambda: self.show_error(message))

    def show_photo(self, path):
        self.photo_path = path
        self.clear_screen()

        image = Image.open(path)
        image.thumbnail((540, 340))

        self.image_ref = ImageTk.PhotoImage(image)

        tk.Label(
            self.root,
            image=self.image_ref,
            bg="#181827"
        ).pack(pady=10)

        self.make_button(
            "TAKE ANOTHER",
            self.show_home
        ).pack(pady=10)

    def show_error(self, message):
        self.clear_screen()
        self.make_label("Camera error", 26).pack(pady=25)

        tk.Label(
            self.root,
            text=message,
            fg="white",
            bg="#181827",
            wraplength=700
        ).pack(pady=10)

        self.make_button("BACK", self.show_home).pack(pady=10)
