import torch

from transformers import VitMatteImageProcessor, VitMatteForImageMatting
from PIL import Image
from _utils import get_image_names_with_ext_from_folder

def generate_alpha_matte(input_dir, descaled_dir, trimap_dir, alpha_matte_dir):
    print('Initiating the process to generate the alpha matte using ViTMatte')
    image_names_with_ext = get_image_names_with_ext_from_folder(input_dir)

    """
    # Method 1: Using hugging face requires active internet connection for each run:
    processor = VitMatteImageProcessor.from_pretrained("hustvl/vitmatte-small-composition-1k")
    model = VitMatteForImageMatting.from_pretrained("hustvl/vitmatte-small-composition-1k")
    # or,
    processor = VitMatteImageProcessor.from_pretrained("hustvl/vitmatte-base-composition-1k")
    model = VitMatteForImageMatting.from_pretrained("hustvl/vitmatte-base-composition-1k")
    """

    # Method 2: Download three files: 1. config.json 2. preprocessor_config.json and 3. pytorch_model.bin
    # from https://huggingface.co/hustvl/vitmatte-base-composition-1k/tree/main and save it in ./checkpoints folder
    # This avoids using internet for each run
    processor = VitMatteImageProcessor.from_pretrained("./checkpoints/")
    model = VitMatteForImageMatting.from_pretrained("./checkpoints/")

    for image_name_with_ext in image_names_with_ext:
        image_name = image_name_with_ext.split('.')[0]
        descaled_img_name = f'{image_name}_desc.png'
        trimap_name = f'{image_name}_trimap.png'
        alpha_matte_name = f'{image_name}_alpha.png'

        # image_path = f'{input_dir}{image_name_with_ext}'
        descaled_img_path = f'{descaled_dir}/{descaled_img_name}'
        trimap_path = f'{trimap_dir}/{trimap_name}'
        alpha_matte_path = f'{alpha_matte_dir}/{alpha_matte_name}'

        print(f'Processing image: {image_name_with_ext} and its trimap: {trimap_name}')

        # image = Image.open(image_path).convert("RGB")
        image = Image.open(descaled_img_path).convert("RGB")
        trimap = Image.open(trimap_path).convert("L")

        # prepare image + trimap for the model
        inputs = processor(images=image, trimaps=trimap, return_tensors="pt")

        with torch.no_grad():
            alphas = model(**inputs).alphas

        image_array = alphas.squeeze().numpy()
        image_pil = Image.fromarray((image_array * 255).astype('uint8'), 'L')

        image_pil.show()
        image_pil.save(alpha_matte_path, 'PNG', compress_level = 0) # Lossless or no compression

        print('Alpha matte is generated for the given image and its trimap')