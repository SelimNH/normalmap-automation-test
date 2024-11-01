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
    print(image)
    img = Image.open(image)
    img_name = image.split("/")[-1]
    normal_img = create_normal_map_pil_img(img)
    normal_img_path = os.path.join(output_folder, img_name.replace(".png", "-normal.png"))
    normal_img.save(normal_img_path)

