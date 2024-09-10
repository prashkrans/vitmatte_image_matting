from generate_trimap import generate_trimap
from generate_alpha_matte import generate_alpha_matte
from crop_using_alpha_matte import create_cropped_image
import tkinter as tk
from utils import input_dir, output_dir, trimap_dir, descaled_dir, alpha_matte_dir, clear_image_files
from upload_images import ImageUploaderApp
from download_images import ImageDownloaderApp

if __name__ == "__main__":
    dirs = [input_dir, output_dir, trimap_dir, descaled_dir, alpha_matte_dir]
    for dir in dirs:
        clear_image_files(dir)
    root = tk.Tk()
    uploader_app = ImageUploaderApp(root)
    root.mainloop()
    generate_trimap(input_dir, descaled_dir, trimap_dir)
    generate_alpha_matte(input_dir, descaled_dir, trimap_dir, alpha_matte_dir)
    create_cropped_image(input_dir, descaled_dir, alpha_matte_dir, output_dir)
    root = tk.Tk()
    downloader_app = ImageDownloaderApp(root)
    root.mainloop()