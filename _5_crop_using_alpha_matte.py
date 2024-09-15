from PIL import Image
from _utils import get_image_names_with_ext_from_folder

def create_cropped_image(input_dir, descaled_dir, alpha_matte_dir, output_dir):
    print('Initiating the cropping process using the generated alpha matte')
    image_names_with_ext = get_image_names_with_ext_from_folder(input_dir)

    for image_name_with_ext in image_names_with_ext:
        image_name = image_name_with_ext.split('.')[0]
        descaled_img_name = f'{image_name}_desc.png'
        alpha_matte_name = f'{image_name}_alpha.png'
        output_name = f'{image_name}_output.png'

        # image_path = f'{input_dir}{image_name_with_ext}'
        descaled_img_path = f'{descaled_dir}/{descaled_img_name}'
        alpha_matte_path = f'{alpha_matte_dir}/{alpha_matte_name}'
        output_path = f'{output_dir}/{output_name}'

        print(f'Cropping the current image: {image_name_with_ext} with its alpha matte: {alpha_matte_name}')

        # Open the image and alpha matte
        # image = Image.open(image_path)
        image = Image.open(descaled_img_path)
        alpha_matte = Image.open(alpha_matte_path)

        # Create a new image with RGBA mode with dimensions of the source image
        cropped_image = Image.new("RGBA", image.size)

        # Iterate through each pixel in source image
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                # Get the alpha value from the alpha matte
                alpha_value = alpha_matte.getpixel((x, y))

                # Get the RGB values from the original image
                rgb_values = image.getpixel((x, y))

                # Create a new pixel with the same RGB values and the alpha value from the matte
                new_pixel = (rgb_values[0], rgb_values[1], rgb_values[2], alpha_value)

                # Put the new pixel in the cropped image
                cropped_image.putpixel((x, y), new_pixel)

        # Save the cropped image
        cropped_image.show()
        cropped_image.save(output_path, "PNG")
        print(f'The cropped image is saved successfully at {output_path}')
