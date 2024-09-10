# Image Matting Python App using ViTMatte
- Given a single or multiple images, this tool allows the user to paint a trimap. Using the source images along with their trimaps, two results can be generated:
a. an image with the background removed, and
b. the alpha matte (Black and White Contour).
- A trimap is a grayscale image used in image segmentation or matting, where pixels are categorized into three regions: white (foreground), black (background), and grey (unknown). The white and black areas are clearly identified, while the grey regions are where the algorithm determines whether the pixel belongs to the foreground or background. This helps in accurately separating objects from their backgrounds.
- The source image, along with the trimap, can then be fed into image matting models such as ViTMatte.
- Image matting is a technique used to accurately separate the foreground (such as a person or object) from the background in an image.
- This is particularly useful in tasks like creating transparent backgrounds, adding effects, or changing the background in photos and videos.
- ViTMatte can achieve precise and high-quality matting results, even in challenging scenarios like hair or semi-transparent objects.

### Demo Video:
https://github.com/user-attachments/assets/f0a024ac-c02c-47a8-b3d4-e952edd077ee

### Prerequisites:
- Python 3.11 (Might work with lower/higher versions as well)
- Hugging Face Hub
- tkinter (Only for linux): `sudo apt install python3-tk`
- I have not tested for NVIDIA cuda, may be significantly faster.
- Critical Resolution kept as 1536 (2048 works but is painfully slow and > 2048 gives an error as it requires more RAM)

### Setup:
1. Clone the repo and move to the root dir.
```commandline
git clone https://github.com/prashkrans/viTmatte_using_hf.git
cd viTmatte_using_hf/
```
2. Create a python virtual environment.
```commandline
python3 -m venv env_vit
source env_vit/bin/activate
```
3. Install the requirements (Might take some time).   
```
sudo apt install python3-tk
pip install -r requirements.txt
```

### Usage:
1. Run `python3 main.py`.
2. Upload single or multiple images.
3. Paint trimaps sequentially for all the uploaded images.
4. Wait for the processing to complete after which two results would be obtained: a. an image with background removed and b. the alpha matte (Black and White Contour). These would also be saved at `output_dir` and `alpha_matte_dir` respectively, which could be downloaded at <date-time>_output_dir and <date_time>_alpha_matte_dir.

### Quick setup and usage for Windows:
1. Install git from https://git-scm.com/download/win
2. Install python 3.10 from MS Store (not python.org)
3. Run `setup.bat` inside `C:\Workspace\image_matting\` (Only once). You may change the path but update the same in `run.bat` as well. 
4. Run `run.bat` and click on upload images to upload single or multiple image(s) | This currently works for the path `C:\Workspace\image_matting\viTmatte_using_hf`
5. Paint trimap for the image(s)
6. Wait for procesing until prompted to download the final images without background along with their alpha matte images

**Note:** Although critical_resolution of 2048 works, its really slow, so don't increase the value above 1536.

### Trimap Keybinds:
1. Q or 1 => Grey Mask (Unknown Region)
2. E or 2 => White Mask (Foreground)
3. Up arrow or +/= => Increases the brush size
4. Down arrow or _/- => Decreases the brush size
5. Enter => Saves the trimap
6. Esc => Reverts all the changes

### Note:
- Descale option is used to avoid `CUDA OOM`.
- Dev Options: Feel free to play with `critical_pixel = 1024` in line 12 of `descale_image.py` to have larger image resolution as output or use an upscaler.
- Currently, it doesn't support undo, so if the trimap gets messed up, you'd have to start over by pressing the `Esc` key.
- There are two ways to use VitMatte:
  1. ViTMatte from hugging faces | Tested, works really great 
  2. ViTMatte from github - Yet to test


### License:
This app and ViTMatte's model weights are released under the MIT License. See [LICENSE](LICENSE) for further details.

### Credits:
1. [ViTMatte (Hugging Face Page)](https://huggingface.co/docs/transformers/en/model_doc/vitmatte)


