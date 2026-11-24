
import tkinter as tk
from ui import PhotoBooth


def main():
    root = tk.Tk()
    app = PhotoBooth(root)
    root.mainloop()


if __name__ == "__main__":
    main()
