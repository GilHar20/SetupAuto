import bpy
import re
from collections import defaultdict



class SETUPAUTO_OT_patternsdetection(bpy.types.Operator):
    '''Class finds patterns in objects names as strings'''
    bl_idname = "setupauto.ot_patternsdetection"
    bl_label = "Patterns Detection"
    bl_description = "Operator loops through selected objects, finding string patterns in their names"



    def clean_string(self, string):
        """Remove numerics, spaces, and special characters"""
        # Remove numbers, spaces, and special characters
        cleaned = re.sub(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', '', string)
        return cleaned.lower()  # Convert to lowercase for consistency

    def is_pattern_contained(self, pattern, existing_patterns):
        """Check if pattern is contained within any existing pattern"""
        for existing in existing_patterns:
            if pattern in existing:
                return True
        return False

    def find_largest_prefixes(self, cleaned_strings, original_mapping):
        """Find largest possible prefix patterns"""
        # Get all possible prefixes
        prefix_count = defaultdict(set)
        
        for cleaned, originals in original_mapping.items():
            for length in range(1, len(cleaned) + 1):
                prefix = cleaned[:length]
                if len(prefix) >= 2:  # Minimum 2 characters
                    prefix_count[prefix].update(originals)
        
        # Sort by length (longest first) and count
        all_prefixes = [(prefix, objects) for prefix, objects in prefix_count.items() 
                       if len(objects) >= 10]
        all_prefixes.sort(key=lambda x: (len(x[1]), len(x[0])), reverse=True)
        
        # Keep only largest patterns that don't contain each other
        largest_patterns = []
        for prefix, objects in all_prefixes:
            if not self.is_pattern_contained(prefix, [p[0] for p in largest_patterns]):
                largest_patterns.append((prefix, objects))
        
        return largest_patterns

    def find_numeric_patterns_for_group(self, original_names):
        """Find numeric patterns within a specific group of original names"""
        numeric_patterns = defaultdict(list)
        
        for name in original_names:
            # Create pattern by replacing numbers with placeholders
            pattern = re.sub(r'\d+', '#', name)
            numeric_patterns[pattern].append(name)
        
        # Sort by count and pattern length
        all_numeric = [(pattern, objects) for pattern, objects in numeric_patterns.items() 
                      if len(objects) >= 2]
        all_numeric.sort(key=lambda x: (len(x[1]), len(x[0])), reverse=True)
        
        # Keep only largest patterns that don't contain each other
        largest_numeric = []
        for pattern, objects in all_numeric:
            # Check if this pattern is contained in any existing pattern
            contained = False
            for existing_pattern, _ in largest_numeric:
                # Compare patterns for containment
                if self.is_numeric_pattern_contained(pattern, existing_pattern):
                    contained = True
                    break
            
            if not contained:
                largest_numeric.append((pattern, objects))
        
        return largest_numeric

    def is_numeric_pattern_contained(self, pattern1, pattern2):
        """Check if one numeric pattern is contained within another"""
        # Simple containment check for numeric patterns
        return pattern1 in pattern2 or pattern2 in pattern1

    def redesigned_pattern_detection(self, object_names):
        """Completely redesigned pattern detection algorithm"""
        # Early exit for small datasets
        if len(object_names) < 10:
            print(f"   Skipping analysis for small dataset ({len(object_names)} objects)")
            return []
        
        print(f"\n=== STEP 1: SAVE ORIGINAL STRINGS ===")
        original_strings = object_names.copy()
        print(f"   Saved {len(original_strings)} original strings")
        
        print(f"\n=== STEP 2: CLEAN STRINGS ===")
        # Create mapping from cleaned string to original strings
        original_mapping = defaultdict(list)
        
        for original in original_strings:
            cleaned = self.clean_string(original)
            if len(cleaned) >= 2:  # Only keep meaningful cleaned strings
                original_mapping[cleaned].append(original)
        
        print(f"   Cleaned to {len(original_mapping)} unique patterns")
        
        print(f"\n=== STEP 3: FIND LARGEST PREFIX PATTERNS ===")
        largest_prefixes = self.find_largest_prefixes(list(original_mapping.keys()), original_mapping)
        
        print(f"   Found {len(largest_prefixes)} largest prefix patterns:")
        for prefix, objects in largest_prefixes:
            print(f"      '{prefix}': {len(objects)} objects")
        
        print(f"\n=== STEP 4: FIND NUMERIC PATTERNS FOR EACH PREFIX ===")
        final_results = []
        
        for prefix, objects in largest_prefixes:
            print(f"\n   Processing prefix '{prefix}' with {len(objects)} objects:")
            
            # Find numeric patterns within this group
            numeric_patterns = self.find_numeric_patterns_for_group(list(objects))
            
            result_entry = {
                "prefix_pattern": prefix,
                "prefix_objects": list(objects),
                "prefix_count": len(objects),
                "numeric_patterns": []
            }
            
            for numeric_pattern, numeric_objects in numeric_patterns:
                result_entry["numeric_patterns"].append({
                    "pattern": numeric_pattern,
                    "objects": numeric_objects,
                    "count": len(numeric_objects)
                })
                print(f"      Numeric pattern '{numeric_pattern}': {len(numeric_objects)} objects")
            
            if not result_entry["numeric_patterns"]:
                print(f"      No numeric patterns found")
            
            final_results.append(result_entry)
        
        return final_results

    def apply_patterns_to_ui(self, context, final_results):
        """Apply detected patterns to UI pattern properties"""
        if not final_results:
            print("No patterns to apply to UI")
            return
        
        pattern_props = context.scene.pattern_props
        
        # Clear existing patterns
        pattern_props.clear()
        
        # Count total patterns to create
        total_patterns = 0
        for result_entry in final_results:
            if result_entry["numeric_patterns"]:
                # Add numeric patterns
                total_patterns += len(result_entry["numeric_patterns"])
            else:
                # Add prefix pattern if no numeric patterns found
                total_patterns += 1
        
        print(f"\n=== APPLYING {total_patterns} PATTERNS TO UI ===")
        
        # Create pattern entries
        pattern_index = 0
        for result_entry in final_results:
            if result_entry["numeric_patterns"]:
                # Add each numeric pattern
                for numeric_pattern in result_entry["numeric_patterns"]:
                    # Add new pattern to collection
                    bpy.ops.setupauto.add_pattern()
                    
                    # Get the newly added pattern
                    new_pattern = pattern_props[pattern_index]
                    
                    # Set pattern_sample to the detected pattern
                    new_pattern.pattern_sample = numeric_pattern["pattern"]
                    
                    # Leave pattern_name empty as requested
                    new_pattern.pattern_name = ""
                    
                    # Don't change pattern_action and parent_collection (keep defaults)
                    
                    print(f"   Applied pattern {pattern_index + 1}: '{numeric_pattern['pattern']}'")
                    pattern_index += 1
            else:
                # Add prefix pattern if no numeric patterns found
                # Add new pattern to collection
                bpy.ops.setupauto.add_pattern()
                
                # Get the newly added pattern
                new_pattern = pattern_props[pattern_index]
                
                # Set pattern_sample to the prefix pattern
                new_pattern.pattern_sample = result_entry["prefix_pattern"]
                
                # Leave pattern_name empty as requested
                new_pattern.pattern_name = ""
                
                # Don't change pattern_action and parent_collection (keep defaults)
                
                print(f"   Applied pattern {pattern_index + 1}: '{result_entry['prefix_pattern']}'")
                pattern_index += 1
        
        print(f"Successfully applied {total_patterns} patterns to UI")

    def execute(self, context):
        """Operator finds patterns in objects names as strings"""
        
        if not context.selected_objects:
            print("No objects selected")
            return {'FINISHED'}
        
        # Extract object names
        object_names = [obj.name for obj in context.selected_objects if obj.name]
        
        if len(object_names) < 2:
            print("Need at least 2 objects to detect patterns")
            return {'FINISHED'}
        
        print(f"\n=== REDESIGNED PATTERN DETECTION ANALYSIS ===")
        print(f"Analyzing {len(object_names)} object names")
        
        # Perform redesigned pattern detection
        final_results = self.redesigned_pattern_detection(object_names)
        
        # Display final results
        print(f"\n=== FINAL RESULTS (2D ARRAY STRUCTURE) ===")
        if not final_results:
            print("No significant patterns detected")
        else:
            print(f"Found {len(final_results)} prefix patterns with numeric sub-patterns:")
            
            for i, result in enumerate(final_results):
                print(f"\n{i+1}. PREFIX PATTERN: '{result['prefix_pattern']}'")
                print(f"   Objects: {result['prefix_count']} total")
                print(f"   Numeric sub-patterns: {len(result['numeric_patterns'])}")
                
                for j, numeric in enumerate(result['numeric_patterns']):
                    print(f"   {i+1}.{j+1} NUMERIC: '{numeric['pattern']}'")
                    print(f"        Objects ({numeric['count']}): {', '.join(numeric['objects'][:5])}{'...' if len(numeric['objects']) > 5 else ''}")
                
                if not result['numeric_patterns']:
                    print(f"   (No numeric patterns found for this prefix)")
        
        # Apply detected patterns to UI
        self.apply_patterns_to_ui(context, final_results)
        
        return {'FINISHED'}