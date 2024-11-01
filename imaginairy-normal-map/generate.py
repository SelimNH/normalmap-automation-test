import os
import sys
from PIL import Image
from imaginairy_normal_map.model import create_normal_map_pil_img
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Utils import utils

images_path = utils.list_images()
output_folder = "./output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for image in images_path:
    img_name = os.path.basename(image)
    normal_img_path = os.path.join(output_folder, img_name.replace(".png", "-normal.png"))
    print(f"Generating normal map for {img_name} to {normal_img_path}")

    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
        print(f"Converted {img_name} to RGB")

    normal_img = create_normal_map_pil_img(img)
    normal_img.save(normal_img_path)
