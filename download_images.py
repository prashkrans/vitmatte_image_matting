import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import os
import shutil
from datetime import datetime


class ImageDownloader:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Downloader")
        self.master.geometry("600x400")

        style = ttk.Style("darkly")

        output_dir = "./resources/output_dir"
        alpha_matte_dir = "./resources/alpha_matte_dir"

        self.unique_prefix = self.generate_unique_prefix()
        self.unique_output_dir = f"../Downloads/{self.unique_prefix}_output"
        self.unique_alpha_matte_dir = f"../Downloads/{self.unique_prefix}_alpha_matte"

        os.makedirs(self.unique_output_dir, exist_ok=True)
        os.makedirs(self.unique_alpha_matte_dir, exist_ok=True)

        self.create_widgets(output_dir, alpha_matte_dir)

    def create_widgets(self, output_dir, alpha_matte_dir):
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        title_label = ttk.Label(
            main_frame,
            text="Image Downloader",
            font=("TkDefaultFont", 24, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(pady=(0, 20))

        self.output_button = ttk.Button(
            main_frame,
            text="Download output images",
            command=lambda: self.download_images(output_dir, self.unique_output_dir),
            bootstyle="success-outline",
            width=25
        )
        self.output_button.pack(pady=10)

        self.alpha_matte_button = ttk.Button(
            main_frame,
            text="Download alpha mattes",
            command=lambda: self.download_images(alpha_matte_dir, self.unique_alpha_matte_dir),
            bootstyle="info-outline",
            width=25
        )
        self.alpha_matte_button.pack(pady=10)

        self.status_label = ttk.Label(
            main_frame,
            text="No downloads yet",
            bootstyle="inverse-secondary"
        )
        self.status_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(
            main_frame,
            bootstyle="success-striped",
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)

    def generate_unique_prefix(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def download_images(self, source_dir, destination_dir):
        if not os.path.exists(source_dir):
            Messagebox.show_error(f"Source directory does not exist: {source_dir}", "Error")
            return

        try:
            files_to_copy = [f for f in os.listdir(source_dir) if self.is_image_file(f)]
            total_files = len(files_to_copy)

            if total_files == 0:
                Messagebox.show_info("No images found to download.", "Info")
                self.status_label.config(text="No images found to download")
                return

            self.progress_bar['maximum'] = total_files
            files_copied = 0

            for filename in files_to_copy:
                source_path = os.path.join(source_dir, filename)
                dest_path = os.path.join(destination_dir, filename)
                shutil.copy2(source_path, dest_path)
                files_copied += 1
                self.progress_bar['value'] = files_copied
                self.status_label.config(text=f"Downloading: {files_copied}/{total_files}")
                self.master.update_idletasks()

            Messagebox.show_info(f"{files_copied} image(s) downloaded successfully!", "Success")
            self.status_label.config(text=f"{files_copied} image(s) downloaded to {destination_dir}")

        except Exception as e:
            Messagebox.show_error(f"An error occurred: {str(e)}", "Error")
            self.status_label.config(text="Download failed")

        finally:
            self.progress_bar['value'] = 0

    def is_image_file(self, filename):
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        return os.path.splitext(filename)[1].lower() in image_extensions


if __name__ == "__main__":
    root = ttk.Window()
    app = ImageDownloader(root)
    root.mainloop()