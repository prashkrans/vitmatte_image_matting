import tkinter as tk
from tkinter import messagebox
import os
import shutil
from datetime import datetime

class ImageDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Downloader")
        self.master.geometry("600x400")

        output_dir = "./resources/output_dir"
        alpha_matte_dir = "./resources/alpha_matte_dir"

        self.unique_prefix = self.generate_unique_prefix()
        self.unique_output_dir = f"../Downloads/{self.unique_prefix}_output"
        self.unique_alpha_matte_dir = f"../Downloads/{self.unique_prefix}_alpha_matte"

        os.makedirs(self.unique_output_dir, exist_ok=True)
        os.makedirs(self.unique_alpha_matte_dir, exist_ok=True)

        self.create_widgets(output_dir, alpha_matte_dir)

    def create_widgets(self, output_dir, alpha_matte_dir):
        self.output_button = tk.Button(
            self.master,
            text="Download output images",
            command=lambda: self.download_images(output_dir, self.unique_output_dir)
        )
        self.output_button.pack(pady=20)

        self.alpha_matte_button = tk.Button(
            self.master,
            text="Download alpha mattes",
            command=lambda: self.download_images(alpha_matte_dir, self.unique_alpha_matte_dir)
        )
        self.alpha_matte_button.pack(pady=20)

        self.status_label = tk.Label(self.master, text="")
        self.status_label.pack(pady=10)

    def generate_unique_prefix(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def download_images(self, source_dir, destination_dir):
        if not os.path.exists(source_dir):
            messagebox.showerror("Error", f"Source directory does not exist: {source_dir}")
            return

        try:
            files_copied = 0
            for filename in os.listdir(source_dir):
                if self.is_image_file(filename):
                    source_path = os.path.join(source_dir, filename)
                    dest_path = os.path.join(destination_dir, filename)
                    shutil.copy2(source_path, dest_path)
                    files_copied += 1

            if files_copied > 0:
                messagebox.showinfo("Success", f"{files_copied} image(s) downloaded successfully!")
                self.status_label.config(text=f"{files_copied} image(s) downloaded to {destination_dir}")
            else:
                messagebox.showinfo("Info", "No images found to download.")
                self.status_label.config(text="No images found to download")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Download failed")

    def is_image_file(self, filename):
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        return os.path.splitext(filename)[1].lower() in image_extensions

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDownloaderApp(root)
    root.mainloop()