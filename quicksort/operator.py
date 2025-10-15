import bpy



class SETUPAUTO_OT_quicksort(bpy.types.Operator):
    '''Class sorts objects'''
    bl_idname = "setupauto.ot_quicksort"
    bl_label = "Sort objects"
    bl_description = "Operator sorts all MESH objects in scene into collection based on string patterns"
    bl_options = {'REGISTER', 'UNDO'}


    def get_collection(self, context, pattern_entry):
        """Get existing collection or create new one with proper parent"""
        quicksort_props = context.scene.quicksort_props

        if pattern_entry.output_collection in bpy.data.collections:
            pattern_collection = bpy.data.collections[pattern_entry.output_collection]
            return pattern_collection
        else:
            pattern_collection = bpy.data.collections.new(pattern_entry.pattern_sample)

        main_collection = quicksort_props.main_collection
        parent_collection = pattern_entry.parent_collection

        match (bool(main_collection), bool(parent_collection)):
            case (False, False):
                context.scene.collection.children.link(pattern_collection)
                self.report({'INFO'}, "case 1")
            case (True, False):
                main_collection.children.link(pattern_collection)
                self.report({'INFO'}, "case 2")
            case (False, True):
                parent_collection.children.link(pattern_collection)
                self.report({'INFO'}, "case 3")
            case (True, True):
                if parent_collection.name in main_collection.children:
                    pass
                else:    
                    main_collection.children.link(parent_collection)
                parent_collection.children.link(pattern_collection)
                self.report({'INFO'}, "case 4")

        return pattern_collection


    def organize_objects(self, context, pattern_entry, i):
        """Organize objects into collections based on pattern"""
        collection = self.get_collection(context, pattern_entry)
                       
        for obj in bpy.context.selected_objects:
            originalCollection = obj.users_collection[0]
            originalCollection.objects.unlink(obj)
            collection.objects.link(obj)
        
        print(f"Iteration {i+1}: Objects organized into collection: {pattern_entry.output_collection}")


    def rename_objects(self, context, pattern_entry, i):
        """Organize objects into collections based on pattern"""
        collection = self.get_collection(context, pattern_entry)
                       
        for obj in bpy.context.selected_objects:
            # Added line for renaming
            obj.name = f"{pattern_entry.new_name}.{i+1:03d}"

            originalCollection = obj.users_collection[0]
            originalCollection.objects.unlink(obj)
            collection.objects.link(obj)
        
        print(f"Iteration {i+1}: Objects organized into collection: {pattern_entry.output_collection}")


    def join_objects(self, context, pattern_entry, i):
        """Join objects together and organize into collection"""
        selected_objects = list(bpy.context.selected_objects)
        
        if len(selected_objects) < 2:
            print(f"Iteration {i+1}: Less than 2 objects selected, nothing to join")
            return
            
        collection = self.get_collection(context, pattern_entry)
        
        bpy.context.view_layer.objects.active = selected_objects[0]
        
        bpy.ops.object.join()
        
        joined_object = bpy.context.active_object
        if joined_object:
            originalCollection = joined_object.users_collection[0]
            originalCollection.objects.unlink(joined_object)
            collection.objects.link(joined_object)
        
        print(f"Iteration {i+1}: {len(selected_objects)} objects joined and organized into collection: {pattern_entry.output_collection}")


    def delete_objects(self, context, pattern_entry, i):
        """Delete selected objects"""
        selected_objects = list(bpy.context.selected_objects)
        for obj in selected_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        
        print(f"Iteration {i+1}: {len(selected_objects)} objects deleted using pattern: {pattern_entry.pattern_sample}")


    def execute(self, context):
        pattern_props = context.scene.pattern_props
        
        if not pattern_props:
            self.report({'INFO'}, "No pattern properties defined, cancelled.")
            return {'CANCELLED'}

        used_pattern_samples = set()

        # Run the pattern operation for each item in the collection
        for i, pattern_entry in enumerate(pattern_props):
            if not pattern_entry.pattern_sample:
                print(f"Iteration {i+1}: Skipped, missing pattern sample.")
                continue

            if pattern_entry.pattern_sample in used_pattern_samples:
                print(f"Iteration {i+1}: Skipped - pattern sample '{pattern_entry.pattern_sample}' was already used.")
                continue

            used_pattern_samples.add(pattern_entry.pattern_sample)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern="*" + pattern_entry.pattern_sample + "*")

            match pattern_entry.pattern_action:
                case 'ORGANIZE':
                    self.organize_objects(context, pattern_entry, i)
                case 'RENAME':
                    self.rename_objects(context, pattern_entry, i)
                case 'JOIN':
                    self.join_objects(context, pattern_entry, i)
                case 'DELETE':
                    self.delete_objects(context, pattern_entry, i)

            bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}
