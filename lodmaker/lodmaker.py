from typing import Self
import bpy
import bmesh
from mathutils import Vector


def duplicate_object(obj):
    """Create a duplicate of the given object and apply convex hull."""
    # Create a copy of the object
    duplicate = obj.copy()
    duplicate.data = obj.data.copy()
    #duplicate.name = obj.name + "_LOD"
    
    # Link the duplicate to the scene
    bpy.context.collection.objects.link(duplicate)
    
    # Apply convex hull using bpy.ops
    bpy.context.view_layer.objects.active = duplicate
    duplicate.select_set(True)
    
    # Enter edit mode and apply convex hull
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.convex_hull()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = duplicate
    
    return duplicate


def make_material_users(obj):
    """Make new users for all materials of the object."""
    if not obj.data.materials:
        Self.report({'INFO'}, "Object has no materials")
        return
    
    new_materials = []
    for material in obj.data.materials:
        new_material = material.copy()
        new_material.name = material.name + "_LOD"
        new_materials.append(new_material)
    
    '''
    # Assign the new materials to the object
    obj.data.materials.clear()
    for material in new_materials:
        obj.data.materials.append(material)
    '''


def get_texture_average_rgb(texture):
    """Calculate the average RGB value of a texture."""
    if not texture or not hasattr(texture, 'image') or not texture.image:
        return (0.5, 0.5, 0.5)  # Default gray color
    
    image = texture.image
    if not image.pixels:
        return (0.5, 0.5, 0.5)
    
    # Get image pixels as a list
    pixels = list(image.pixels)
    
    # Get image dimensions
    width, height = image.size
    channels = len(pixels) // (width * height)
    
    # Calculate average RGB values
    total_r = 0.0
    total_g = 0.0
    total_b = 0.0
    pixel_count = width * height
    
    if channels >= 3:
        # RGBA format - take first 3 channels
        for i in range(0, len(pixels), channels):
            total_r += pixels[i]     # Red
            total_g += pixels[i + 1] # Green
            total_b += pixels[i + 2] # Blue
    else:
        # Grayscale image
        for i in range(0, len(pixels), channels):
            gray_value = pixels[i]
            total_r += gray_value
            total_g += gray_value
            total_b += gray_value
    
    avg_r = total_r / pixel_count
    avg_g = total_g / pixel_count
    avg_b = total_b / pixel_count
    
    return (avg_r, avg_g, avg_b)


def replace_textures_with_rgb(material):
    """Replace all texture nodes with RGB nodes using average colors."""
    if not material or not material.use_nodes:
        return
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Find all texture nodes
    texture_nodes = []
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            texture_nodes.append(node)
    
    # Replace each texture node with an RGB node
    for tex_node in texture_nodes:
        # Calculate average RGB of the texture
        avg_rgb = get_texture_average_rgb(tex_node.image)
        
        # Create new RGB node
        rgb_node = nodes.new(type='ShaderNodeRGB')
        rgb_node.location = tex_node.location
        rgb_node.outputs[0].default_value = (*avg_rgb, 1.0)  # RGBA format
        
        # Reconnect all links from the texture node to the RGB node
        for output in tex_node.outputs:
            for link in output.links:
                links.new(rgb_node.outputs[0], link.to_socket)
        
        # Remove the old texture node
        nodes.remove(tex_node)


def execute(self, context):
    """Main function to create LOD object from selected object."""

    obj = bpy.context.active_object
    
    if not obj:
        self.report({'INFO'}, "No active object selected")
        return
    
    if obj.type != 'MESH':
        self.report({'INFO'}, "Selected object is not a mesh")
        return
    
    duplicate = duplicate_object(obj)
    
    # Make new material users
    make_material_users(duplicate)
    
    # Process each material
    for material in duplicate.data.materials:
        if material:
            replace_textures_with_rgb(material)
    
    # Select the new LOD object
    bpy.context.view_layer.objects.active = duplicate
    duplicate.select_set(True)
    
    print(f"Created LOD object: {duplicate.name}")
    return duplicate

    
    def execute(self, context):
        try:
            create_lod_object()
            self.report({'INFO'}, "LOD object created successfully")

        except Exception as e:
            self.report({'ERROR'}, f"Failed to create LOD object: {str(e)}")


execute()