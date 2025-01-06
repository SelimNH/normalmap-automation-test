import argparse
import os
import numpy as np
import imageio.v3 as iio
import module_color_to_normals
import module_normals_to_curvature
import module_normals_to_height

def process_image(input_path, output_path, module, args):
    # Read input image
    in_img = iio.imread(input_path)
    # Convert from H,W,C in [0, 256] to C,H,W in [0,1]
    in_img = np.transpose(in_img, (2, 0, 1)) / 255

    # Apply processing
    if module == "color_to_normals":
        out_img = module_color_to_normals.apply(
            in_img, args.color_to_normals_overlap, None
        )
        
    elif module == "normals_to_curvature":
        out_img = module_normals_to_curvature.apply(
            in_img, args.normals_to_curvature_blur_radius, None
        )
    elif module == "normals_to_height":
        out_img = module_normals_to_height.apply(
            in_img, args.normals_to_height_seamless == "TRUE", None
        )
    else:
        raise ValueError(f"Unknown module: {module}")

    # Convert from C,H,W in [0,1] to H,W,C in [0, 256]
    out_img = (np.transpose(out_img, (1, 2, 0)) * 255).astype(np.uint8)
    # Write output image
    iio.imwrite(output_path, out_img)

# Parse CLI args
parser = argparse.ArgumentParser(description="DeepBump Batch CLI")
parser.add_argument("input_folder", help="path to the folder containing input images", type=str)
parser.add_argument("output_folder", help="path to the folder for output images", type=str)
parser.add_argument(
    "module",
    help="processing to be applied",
    choices=["color_to_normals", "normals_to_curvature", "normals_to_height"],
)
parser.add_argument(
    "--verbose",
    action=argparse.BooleanOptionalAction,
    help="prints progress to the console",
)
parser.add_argument(
    "--color_to_normals-overlap",
    choices=["SMALL", "MEDIUM", "LARGE"],
    required=False,
    default="LARGE",
)
parser.add_argument(
    "--normals_to_curvature-blur_radius",
    choices=["SMALLEST", "SMALLER", "SMALL", "MEDIUM", "LARGE", "LARGER", "LARGEST"],
    required=False,
    default="MEDIUM",
)
parser.add_argument(
    "--normals_to_height-seamless",
    choices=["TRUE", "FALSE"],
    required=False,
    default="FALSE",
)
args = parser.parse_args()

# Ensure output folder exists
os.makedirs(args.output_folder, exist_ok=True)

# Iterate over all files in the input folder and its subfolders
for root, dirs, files in os.walk(args.input_folder):
    for filename in files:
        input_path = os.path.join(root, filename)

        # Skip any non-image files
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            if args.verbose:
                print(f"Skipping non-image file: {input_path}")
            continue

        # Determine the relative subfolder path (e.g., "grass" if root is "Inputs/grass")
        rel_dir = os.path.relpath(root, args.input_folder)

        # Create a matching subfolder under the main output folder (e.g., "Outputs/NormalMaps/grass")
        output_subdir = os.path.join(args.output_folder, rel_dir)
        os.makedirs(output_subdir, exist_ok=True)

        # Extract the base filename (e.g., "image" from "image.png")
        base_name = os.path.splitext(filename)[0]

        # Make another subfolder named after the base filename (e.g., "Outputs/NormalMaps/grass/image")
        base_folder = os.path.join(output_subdir, base_name)
        os.makedirs(base_folder, exist_ok=True)

        # Define the output filename with "-dp" suffix (e.g., "image-dp.png")
        output_filename = f"{base_name}-dp.png"

        # Complete output path (e.g., "Outputs/NormalMaps/grass/image/image-dp.png")
        output_path = os.path.join(base_folder, output_filename)

        if args.verbose:
            print(f"Processing {input_path} -> {output_path}")

        # Process the image and save
        process_image(input_path, output_path, args.module, args)




# python3 batch_generate.py Inputs Outputs color_to_normals --color_to_normals-overlap SMALL --verbose
# python3 batch_generate.py Inputs/TEST Outputs color_to_normals --color_to_normals-overlap SMALL --verbose