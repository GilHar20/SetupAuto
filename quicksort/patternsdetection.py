import bpy
import re
from collections import defaultdict



class SETUPAUTO_OT_patternsdetection(bpy.types.Operator):
    '''Class finds patterns in objects names as strings'''
    bl_idname = "setupauto.ot_patternsdetection"
    bl_label = "Patterns Detection"
    bl_description = "Operator loops through selected objects, finding string patterns in their names"
    bl_options = {'REGISTER', 'UNDO'}



    # pattern detection does the main work in itself.
    # apply_patterns_to_ui is the function that applies the patterns to the UI.
    def pattern_detection(self, object_names):
        """pattern detection algorithm"""

        patterns = set()
        
        for original in object_names:
            string_reformatted = ""
            string_start = False
            words = 0

            for i, char in enumerate(original):
                if re.search(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', char) and string_start == False:
                    continue
                else:
                    if re.search(r'[\s\-_]', char):
                        words += 1
                    string_start = True
                    string_reformatted = string_reformatted + char

                if i + 1 <= len(original)-1:
                    next_char = bool(re.search(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', original[i+1]))
                else:
                    next_char = False

                if i + 2 <= len(original)-1:
                    second_next_char = bool(re.search(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', original[i+2]))
                else:
                    second_next_char = False

                if i + 3 <= len(original)-1:
                    third_next_char = bool(re.search(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', original[i+3]))
                else:
                    third_next_char = False

                if words >= 4:
                    string_start = False
                    break

                if next_char and second_next_char and third_next_char:
                    string_start = False
                    break

            #original = re.sub(r'[0-9,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', '', original)
            patterns.add(string_reformatted)
        
        return patterns


    def apply_patterns_to_ui(self, context, patterns):
        """Apply detected patterns to UI pattern properties"""
        pattern_props = context.scene.pattern_props

        pattern_props.clear()
    
        #pattern_index = 0
        for i, entry in patterns:
            
            bpy.ops.setupauto.add_pattern()
            current_pattern = pattern_props[i]
            current_pattern.output_collection = entry
            current_pattern.pattern_sample = entry

            #pattern_index += 1



    def execute(self, context):
        """Operator finds patterns in objects names as strings"""
        
        if not context.selected_objects:
            self.report({'INFO'}, "No objects selected")
            return {'CANCELLED'}
        
        object_names = [obj.name for obj in context.selected_objects if obj.name]
        
        if len(object_names) <= 10:
            self.report({'INFO'}, "Need at least 11 objects to use pattern detection")
            return {'CANCELLED'}
        
        patterns = list(self.pattern_detection(object_names))
        
        if not patterns:
            self.report({'ERROR'}, "No patterns detected")
            return {'CANCELLED'}
        else:
            self.report({'INFO'}, f"Found {len(patterns)} prefix patterns")

        patterns.sort(key = lambda x: len(x))

        try:
            self.apply_patterns_to_ui(context, patterns)
        except:
            self.report({'ERROR'}, "Failed to apply patterns to UI")
            return {'CANCELLED'}
        
        return {'FINISHED'}