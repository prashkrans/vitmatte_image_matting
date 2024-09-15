import ttkbootstrap as ttk
from _1_upload_images import ImageUploader
from _3_generate_trimap import generate_trimap
from _4_generate_alpha_matte import generate_alpha_matte
from _5_crop_using_alpha_matte import create_cropped_image
from _utils import input_dir, output_dir, trimap_dir, descaled_dir, alpha_matte_dir, clear_image_files
from _6_download_images import ImageDownloader

def process_images():
    generate_trimap(input_dir, descaled_dir, trimap_dir)
    generate_alpha_matte(input_dir, descaled_dir, trimap_dir, alpha_matte_dir)
    create_cropped_image(input_dir, descaled_dir, alpha_matte_dir, output_dir)

def main():
    dirs = [input_dir, output_dir, trimap_dir, descaled_dir, alpha_matte_dir]
    for dir in dirs:
        clear_image_files(dir)

    # Initiate root for uploading images
    root = ttk.Window()
    uploader_app = ImageUploader(root)
    root.mainloop()  # Run the uploader window

    # Process images after upload
    process_images()

    # Use the same root for downloading image
    downloader_app = ImageDownloader(root)

    root.deiconify()  # Show the window
    root.mainloop()  # Run the downloader window

if __name__ == "__main__":
    main()