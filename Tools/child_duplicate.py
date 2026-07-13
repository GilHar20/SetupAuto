import bpy

source = bpy.context.active_object
targets = [obj for obj in bpy.context.selected_objects if obj != source]

children = list(source.children)

for target in targets:
    # Use the first collection the target window belongs to
    collection = target.users_collection[0]

    for child in children:
        new = child.copy()
        if child.data:
            new.data = child.data

        collection.objects.link(new)

        new.parent = target
        new.matrix_parent_inverse = target.matrix_world.inverted()
        new.matrix_local = child.matrix_local