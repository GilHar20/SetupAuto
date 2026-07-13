import bpy
from mathutils import Vector

selected_parents = list(bpy.context.selected_objects)

for old_parent in selected_parents:
    children = list(old_parent.children)

    if not children:
        continue

    # Calculate world-space center of children origins
    center = Vector((0, 0, 0))
    for child in children:
        center += child.matrix_world.translation

    center /= len(children)

    # Create replacement empty
    empty = bpy.data.objects.new(old_parent.name + "_CTRL", None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.matrix_world.translation = center

    # Put empty in the same collections as the old parent
    for coll in old_parent.users_collection:
        coll.objects.link(empty)

    # Reparent children while preserving world transforms
    for child in children:
        world_matrix = child.matrix_world.copy()

        # Assign new parent
        child.parent = empty

        # Remove parent inverse
        child.matrix_parent_inverse.identity()

        # Restore world transform by calculating local transform
        child.matrix_local = empty.matrix_world.inverted() @ world_matrix

    # Optional: remove old empty DXF parent
    # bpy.data.objects.remove(old_parent, do_unlink=True)