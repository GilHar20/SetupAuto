import bpy
import hashlib

def mesh_hash(obj):
    mesh = obj.data
    verts = tuple(round(v.co.x, 6) for v in mesh.vertices) + \
            tuple(round(v.co.y, 6) for v in mesh.vertices) + \
            tuple(round(v.co.z, 6) for v in mesh.vertices)
    materials = tuple(mat.name if mat else "None" for mat in mesh.materials)
    return hashlib.md5(str((verts, materials)).encode()).hexdigest()

def replace_with_instances():
    seen = {}
    for obj in list(bpy.data.objects):
        if obj.type != 'MESH':
            continue
        key = mesh_hash(obj)
        if key not in seen:
            seen[key] = obj
        else:
            ref = seen[key]
            new = bpy.data.objects.new(name=ref.name + "_inst", object_data=ref.data)
            new.matrix_world = obj.matrix_world
            bpy.context.collection.objects.link(new)
            bpy.data.objects.remove(obj)

replace_with_instances()