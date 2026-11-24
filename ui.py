
import tkinter as tk
import threading
from PIL import Image, ImageTk
from camera import take_photo


class PhotoBooth:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photo Booth")

        # Leave room for desktop taskbar and window borders
        self.root.geometry("760x380+10+40")
        self.root.resizable(False, False)
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

    def make_label(self, text, size=22):
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
            font=("Arial", 14, "bold"),
            bg="#e89ab0",
            fg="#181827",
            activebackground="#f4b6ca",
            padx=12,
            pady=5,
            relief="flat"
        )

    def show_home(self):
        self.clear_screen()

        self.make_label(
            "MINI PHOTO BOOTH", 26
        ).pack(pady=(45, 20))

        self.make_button(
            "TAKE PHOTO",
            lambda: self.countdown(3)
        ).pack(pady=10)

        self.make_label(
            "Tap to capture a memory!", 12
        ).pack(pady=5)

        self.make_button(
            "EXIT",
            self.root.destroy
        ).pack(pady=5)

    def countdown(self, number):
        self.clear_screen()

        if number > 0:
            self.make_label(
                "GET READY!", 24
            ).pack(pady=(50, 10))

            self.make_label(
                str(number), 70
            ).pack(pady=5)

            self.root.after(
                1000,
                lambda: self.countdown(number - 1)
            )
        else:
            self.capture()

    def capture(self):
        self.clear_screen()

        self.make_label(
            "Taking your photo...", 22
        ).pack(pady=110)

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
        self.clear_screen()

        self.make_label(
            "YOUR PHOTO!", 20
        ).pack(pady=(5, 5))

        with Image.open(path) as original:
            image = original.copy()

        image.thumbnail((370, 200))
        self.image_ref = ImageTk.PhotoImage(image)

        tk.Label(
            self.root,
            image=self.image_ref,
            bg="#181827"
        ).pack(pady=3)

        self.make_button(
            "TAKE ANOTHER",
            self.show_home
        ).pack(pady=4)

        self.make_button(
            "EXIT",
            self.root.destroy
        ).pack(pady=4)

    def show_error(self, message):
        self.clear_screen()

        self.make_label(
            "Camera Error", 22
        ).pack(pady=(15, 10))

        tk.Label(
            self.root,
            text=message[-500:],
            font=("Arial", 10),
            fg="white",
            bg="#181827",
            wraplength=680,
            justify="center"
        ).pack(pady=5)

        self.make_button(
            "BACK",
            self.show_home
        ).pack(pady=10)

        self.make_button(
            "EXIT",
            self.root.destroy
        ).pack(pady=5)
