from generate_trimap import generate_trimap
from generate_alpha_matte import generate_alpha_matte
from crop_using_alpha_matte import create_cropped_image
from utils import input_dir, descaled_dir, trimap_dir, alpha_matte_dir, output_dir

# image_names_with_ext = get_image_names_with_ext_from_folder(input_dir)
# image_names_with_ext = get_image_names_with_ext_from_folder(input_dir)

if __name__ == "__main__":
    create_trimaps = input('Do you want to create trimaps? (y/n): ')
    if(create_trimaps == ('y' or 'Y')):
        generate_trimap(input_dir, descaled_dir, trimap_dir)
    else:
        print('Skipping creating trimaps as they were already created')

    generate_alpha_matte(input_dir, descaled_dir, trimap_dir, alpha_matte_dir)
    create_cropped_image(input_dir, descaled_dir, alpha_matte_dir, output_dir)