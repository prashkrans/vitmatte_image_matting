import cv2
import numpy as np
from utils import get_image_names_with_ext_from_folder
from math import ceil
from descale_image import descale_image

def generate_trimap(input_dir, descaled_dir, trimap_dir):
    print('Starting trimap generating process')
    print("Create a trimap using 'w' for white color and 'q' for grey color")
    image_names_with_ext = get_image_names_with_ext_from_folder(input_dir)

    for image_name_with_ext in image_names_with_ext:
        print(f'Processing image: {image_name_with_ext}')
        image_path = f'{input_dir}/{image_name_with_ext}'

        image_name = image_name_with_ext.split('.')[0]
        trimap_path = f'{trimap_dir}/{image_name}_trimap.png'
        descaled_img_path = f'{descaled_dir}/{image_name}_desc.png'

        # Read the current image
        img = cv2.imread(image_path)
        img = descale_image(img)

        # Get the original dimensions of the image
        h, w = img.shape[:2]

        cv2.imwrite(descaled_img_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0]) # 0 is lossless

        from PIL import ImageGrab
        import numpy as np

        # Capture the screen
        screen = ImageGrab.grab()

        # Convert the screen capture to a NumPy array
        screen_np = np.array(screen)

        # Get the dimensions
        screen_height, screen_width, _ = screen_np.shape

        max_screen_side_px = max(screen_width, screen_height)
        # FHD = 1920 x 1080 | HD2 = 1366 x 768 | HD = 1280 x 720
        descale_preview_constant = 1280
        if max_screen_side_px == 1920:
            descale_preview_constant = 960
        elif max_screen_side_px == 1366:
            descale_preview_constant = 768
        elif max_screen_side_px == 1280:
            descale_preview_constant = 720
        
        max_side_px = max(w, h)
        descale_preview_factor = max_side_px/descale_preview_constant
        w_pre = int(min(w, w/descale_preview_factor))
        h_pre = int(min(h, h/descale_preview_factor))

        print(f'screen_width: {screen_width}')
        print(f'screen_height: {screen_height}')

        print(f'descale_preview_constant: {descale_preview_constant}')

        print(f'image_width: {w}')
        print(f'image_height: {h}')

        print(f'descale_preview_factor: {descale_preview_factor}')
        print(f'preview_image_width: {w_pre}')
        print(f'preview_image_height: {h_pre}')

        # Create a window to display the image
        cv2.namedWindow("Paint Image", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Paint Image", w, h) # Using w, h of the descaled image which should ideally fit on the screen
        cv2.resizeWindow("Paint Image", w_pre, h_pre) # Using w, h of the descaled image which should ideally fit on the screen
        # cv2.imshow("Paint Image", img)
        cv2.imshow("Paint Image", img)

         # Initialize variables for mouse event
        drawing = False
        height, width = img.shape[:2]
        max_val = max(height, width)

        if  max_val > 4000:
            brush_size = 200  # You can adjust the size of the brush
        elif max_val > 3000:
            brush_size = 120
        elif max_val > 2000:
            brush_size = 75
        elif max_val > 1000:
            brush_size = 30
        else:
            brush_size = 20

        color = (255, 255, 255)  # White color

        # Initialize a mask to track painted pixels
        mask = np.zeros_like(img, dtype=np.uint8)

        # Callback function to handle mouse events
        def draw_circle(event, x, y, flags, param):
            nonlocal drawing, color

            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
            elif event == cv2.EVENT_MOUSEMOVE and drawing:
                # Draw a circle with the current color at the mouse position
                cv2.circle(img, (x, y), brush_size, color, -1)
                cv2.circle(mask, (x, y), brush_size, (255, 255, 255), -1)
                cv2.imshow('Paint Image', img)

        # Set the callback function for mouse events
        cv2.setMouseCallback('Paint Image', draw_circle)

        while True:
            # Display the image and wait for a key press
            cv2.imshow('Paint Image', img)
            key = cv2.waitKey(1) & 0xFF

            # Change color to grey when the user presses 'c' key
            if key == ord('q') or key == ord('1'):
                color = (128, 128, 128)  # Grey color
                brush_size = ceil(0.35 * brush_size)
            elif key == ord('w') or key == ord('2'):
                color = (255, 255, 255)  # White color
                brush_size = ceil(1.5 * brush_size)
            elif key == ord('=') or key == 82:  # Increase brush size by pressing '=' or up arrow)
                brush_size += 2
            elif (key == ord('-') or key == 84) and brush_size > 4:  # Decrease brush size by pressing '-' or down arrow)
                brush_size -= 2
            if key == 27:  # Press 'Esc' to reset the mask
                mask = np.zeros_like(img, dtype=np.uint8)
                img = cv2.imread(image_path)
                cv2.imshow('Paint Image', img)
            # Break the loop if the user presses 'Enter' key and save the trimap so created
            elif key == 13:
                break

        # Set unpainted pixels to black
        unpainted_mask = cv2.bitwise_not(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY))
        img[unpainted_mask > 0] = (0, 0, 0)

        # Save the painted image
        # cv2.imwrite(trimap_path, img)
        cv2.imwrite(trimap_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 3]) # 0 (lossless) to 9 (max compression)

        # Close the OpenCV window
        cv2.destroyAllWindows()

        print(f"Trimap of the image {image_name_with_ext} saved at {trimap_path}")
