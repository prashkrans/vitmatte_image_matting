import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil

from utils import input_dir, clear_image_files


class ImageUploaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Uploader")
        self.master.geometry("600x400")

        self.upload_button = tk.Button(self.master, text="Upload Images", command=self.upload_images)
        self.upload_button.pack(pady=20)

        self.status_label = tk.Label(self.master, text="No images uploaded yet")
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

            messagebox.showinfo("Success", f"{num_images} image(s) uploaded successfully!")
            self.master.destroy()  # Close the window
        else:
            self.status_label.config(text="No images selected")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageUploaderApp(root)
    root.mainloop()