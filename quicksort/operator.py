import bpy



class SETUPAUTO_OT_quicksort(bpy.types.Operator):
    '''Class sorts objects'''
    bl_idname = "setupauto.ot_quicksort"
    bl_label = "Sort objects"
    bl_description = "Operator sorts all MESH objects in scene into collection based on string patterns"

    def get_or_create_collection(self, context, pattern_item):
        """Get existing collection or create new one with proper parent"""
        if pattern_item.pattern_name not in bpy.data.collections:
            collection = bpy.data.collections.new(pattern_item.pattern_name)
            
            # Link to parent collection if specified, otherwise to scene collection
            if pattern_item.parent_collection:
                pattern_item.parent_collection.children.link(collection)
            else:
                context.scene.collection.children.link(collection)
        else:
            collection = bpy.data.collections[pattern_item.pattern_name]
        
        return collection

    def organize_objects(self, context, pattern_item, i):
        """Organize objects into collections based on pattern"""
        collection = self.get_or_create_collection(context, pattern_item)
                                                      
        for obj in bpy.context.selected_objects:
            originalCollection = obj.users_collection[0]
            originalCollection.objects.unlink(obj)
            collection.objects.link(obj)
        
        print(f"Iteration {i+1}: Objects organized into collection: {pattern_item.pattern_name}")

    def join_objects(self, context, pattern_item, i):
        """Join objects together and organize into collection"""
        selected_objects = list(bpy.context.selected_objects)
        
        if len(selected_objects) < 2:
            print(f"Iteration {i+1}: Less than 2 objects selected, nothing to join")
            return
            
        # Create or get collection
        collection = self.get_or_create_collection(context, pattern_item)
        
        # Set first object as active
        bpy.context.view_layer.objects.active = selected_objects[0]
        
        # Join objects
        bpy.ops.object.join()
        
        # Move joined object to collection
        joined_object = bpy.context.active_object
        if joined_object:
            originalCollection = joined_object.users_collection[0]
            originalCollection.objects.unlink(joined_object)
            collection.objects.link(joined_object)
        
        print(f"Iteration {i+1}: {len(selected_objects)} objects joined and organized into collection: {pattern_item.pattern_name}")

    def delete_objects(self, context, pattern_item, i):
        """Delete selected objects"""
        selected_objects = list(bpy.context.selected_objects)
        for obj in selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        
        print(f"Iteration {i+1}: {len(selected_objects)} objects deleted using pattern: {pattern_item.pattern_sample}")

    def execute(self, context):
        pattern_props = context.scene.pattern_props
        
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

            # Handle different actions using match statement
            match pattern_item.pattern_action:
                case 'ORGANIZE':
                    self.organize_objects(context, pattern_item, i)
                case 'JOIN':
                    self.join_objects(context, pattern_item, i)
                case 'DELETE':
                    self.delete_objects(context, pattern_item, i)
                case _:
                    print(f"Iteration {i+1}: Unknown action '{pattern_item.pattern_action}'")
            
            bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}
