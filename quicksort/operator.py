import bpy



class SETUPAUTO_OT_quicksort(bpy.types.Operator):
    '''Class sorts objects'''
    bl_idname = "setupauto.ot_quicksort"
    bl_label = "Sort objects"
    bl_description = "Operator sorts all MESH objects in scene into collection based on string patterns"

    def execute(self, context):
        pattern_props = context.scene.pattern_props

        # match:
        #ORGANIZE
        #JOIN
        #DELETE
        
        if not pattern_props:
            print("No pattern properties defined")
            return {'CANCELLED'}

        # Track used pattern samples to avoid duplicates
        used_pattern_samples = set()

        # Run the pattern operation for each item in the collection
        for i, pattern_item in enumerate(pattern_props):
            # Check if pattern name and sample are available for this iteration
            if not pattern_item.pattern_name or not pattern_item.pattern_sample:
                print(f"Iteration {i+1}: Skipped - missing pattern name or pattern sample")
                continue

            # Check if this pattern sample was already used
            if pattern_item.pattern_sample in used_pattern_samples:
                print(f"Iteration {i+1}: Skipped - pattern sample '{pattern_item.pattern_sample}' was already used in a previous iteration")
                continue

            # Add this pattern sample to used set
            used_pattern_samples.add(pattern_item.pattern_sample)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern="*" + pattern_item.pattern_sample + "*")

            # Check the pattern method and handle accordingly
            if pattern_item.pattern_action == 'ORGANIZE':
                # Proceed with current procedure - organize objects into collections
                if pattern_item.pattern_name not in bpy.data.collections:
                    collection = bpy.data.collections.new(pattern_item.pattern_name)
                    context.scene.collection.children.link(collection)
                else:
                    collection = bpy.data.collections[pattern_item.pattern_name]
                                                          
                for obj in bpy.context.selected_objects:
                    originalCollection = obj.users_collection[0]
                    originalCollection.objects.unlink(obj)
                    collection.objects.link(obj)
                
                print(f"Iteration {i+1}: Objects organized into collection: {pattern_item.pattern_name}")
                
            elif pattern_item.pattern_action == 'DELETE':
                # Delete the selected objects
                selected_objects = list(bpy.context.selected_objects)
                for obj in selected_objects:
                    bpy.data.objects.remove(obj, do_unlink=True)
                
                print(f"Iteration {i+1}: {len(selected_objects)} objects deleted using pattern: {pattern_item.pattern_sample}")
            
            bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}



def register():
    bpy.utils.register_class(SETUPAUTO_OT_quicksort)

def unregister():
    bpy.utils.unregister_class(SETUPAUTO_OT_quicksort)
