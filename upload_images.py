import tkinter as tk
from tkinter import filedialog
import os
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from utils import input_dir, clear_image_files

class CustomMessagebox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        ttk.Label(self, text=message, wraplength=250).pack(pady=20)
        ttk.Button(
            self,
            text="OK",
            command=self.destroy,
            bootstyle="success",
            width=10
        ).pack(pady=10)

        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

class ModernImageUploaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Uploader")
        self.master.geometry("600x400")

        style = ttk.Style("darkly")

        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        title_label = ttk.Label(
            main_frame,
            text="Image Uploader",
            font=("TkDefaultFont", 24, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(pady=20)

        self.upload_button = ttk.Button(
            main_frame,
            text="Upload Images",
            command=self.upload_images,
            bootstyle="success-outline",
            width=20
        )
        self.upload_button.pack(pady=20)

        self.status_label = ttk.Label(
            main_frame,
            text="No images uploaded yet",
            bootstyle="inverse-secondary"
        )
        self.status_label.pack(pady=10)

        os.makedirs(input_dir, exist_ok=True)

    def upload_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_paths:
            clear_image_files(input_dir)

            num_images = len(file_paths)
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                destination = os.path.join(input_dir, filename)
                shutil.copy2(file_path, destination)
                print(f"Copied: {file_path} to {destination}")

            CustomMessagebox(self.master, "Success", f"{num_images} image(s) uploaded successfully!")
            self.master.destroy()  # Close the window
        else:
            self.status_label.config(text="No images selected")

if __name__ == "__main__":
    root = ttk.Window()
    app = ModernImageUploaderApp(root)
    root.mainloop()