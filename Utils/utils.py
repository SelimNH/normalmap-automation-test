import os
from IPython.display import display
from PIL import Image

def list_images():
    images = []
    for root, dirs, files in os.walk("../Inputs"):
        for file in files:
            if file.endswith(".png"):
                images.append(os.path.join(root, file))
    return images