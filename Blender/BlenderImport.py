import os
import bpy

entry_point = "../../../Assets"
current = os.path.abspath(os.path.join(os.getcwd(), entry_point))
print("Current directory:", current)
source_image_path = os.path.join(current, "Prototypes/Graphics/inuhiro_test.png")
output_image_path = os.path.join(current, "Prototypes/Graphics/inuhiro_test_normals.png")

output_image_size = 1024  # Resolution of the normal map

if not os.path.exists(source_image_path):
    print("Source image not found:", source_image_path)
    exit()
else:
    print("Source image found:", source_image_path)

# --- Prepare Scene ---
# Clear all objects in the scene (optional, for a clean start)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add a plane to apply the texture to
bpy.ops.mesh.primitive_plane_add(size=2)
plane = bpy.context.active_object
plane.name = "NormalMapPlane"

# Create a new material
material = bpy.data.materials.new(name="NormalMapMaterial")
material.use_nodes = True
plane.data.materials.append(material)
nodes = material.node_tree.nodes
nodes.clear()

# --- Setup Nodes ---
# Add Image Texture node and load the source image
img_texture_node = nodes.new(type="ShaderNodeTexImage")
img_texture_node.image = bpy.data.images.load(source_image_path)
img_texture_node.image.colorspace_settings.name = 'Non-Color'

# Add Bump node
bump_node = nodes.new(type="ShaderNodeBump")
bump_node.inputs['Strength'].default_value = 1.0  # Adjust as needed

# Connect Image Texture to Bump node
material.node_tree.links.new(img_texture_node.outputs['Color'], bump_node.inputs['Height'])

# Add Principled BSDF and Material Output
bsdf_node = nodes.new(type="ShaderNodeBsdfPrincipled")
output_node = nodes.new(type="ShaderNodeOutputMaterial")

# Connect Bump to Principled BSDF and BSDF to Material Output
material.node_tree.links.new(bump_node.outputs['Normal'], bsdf_node.inputs['Normal'])
material.node_tree.links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

# --- Prepare Bake Target Image ---
# Create a new blank image for baking the normal map
bake_image = bpy.data.images.new("BakedNormalMap", width=output_image_size, height=output_image_size)
bake_image.filepath_raw = output_image_path
bake_image.file_format = 'PNG'
bake_image.colorspace_settings.name = 'Non-Color'

# Assign the bake image to the Image Texture node (target for bake)
img_texture_node.image = bake_image

# --- Set Bake Settings ---
bpy.context.view_layer.objects.active = plane
bpy.context.scene.render.engine = 'CYCLES'

# Ensure the scene is set to bake normal maps with the appropriate settings
bpy.context.scene.cycles.bake_type = 'NORMAL'

# Bake directly using bpy.ops if bake options aren't directly accessible
try:

    bpy.context.scene.cycles.bake.use_clear = True
    bpy.context.scene.cycles.bake.use_selected_to_active = False
except AttributeError:
    print("Warning: bake.clear and bake.use_selected_to_active settings not available; using default baking options.")

# --- Execute Bake ---
bpy.ops.object.bake(type='NORMAL')

# --- Save the Baked Image ---
bake_image.save_render(filepath=output_image_path)

print("Normal map has been baked and saved to:", output_image_path)