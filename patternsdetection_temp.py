import bpy
import re
from collections import defaultdict



def clean_string(string):
    """Remove numerics, spaces, and special characters"""
    # Remove numbers, spaces, and special characters
    cleaned = re.sub(r'[0-9\s\-_,\.\(\)\[\]\{\}<>|/\\:;!@#$%^&*+=`~"\'?]', '', string)
    return cleaned.lower()  # Convert to lowercase for consistency

def is_pattern_contained(pattern, existing_patterns):
    """Check if pattern is contained within any existing pattern"""
    for existing in existing_patterns:
        if pattern in existing:
            return True
    return False

def find_largest_prefixes(cleaned_strings, original_mapping):
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
        if not is_pattern_contained(prefix, [p[0] for p in largest_patterns]):
            largest_patterns.append((prefix, objects))
    
    return largest_patterns

def find_numeric_patterns_for_group(original_names):
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
            if is_numeric_pattern_contained(pattern, existing_pattern):
                contained = True
                break
        
        if not contained:
            largest_numeric.append((pattern, objects))
    
    return largest_numeric

def is_numeric_pattern_contained(pattern1, pattern2):
    """Check if one numeric pattern is contained within another"""
    # Simple containment check for numeric patterns
    return pattern1 in pattern2 or pattern2 in pattern1

def redesigned_pattern_detection(object_names):
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
        cleaned = clean_string(original)
        if len(cleaned) >= 2:  # Only keep meaningful cleaned strings
            original_mapping[cleaned].append(original)
    
    print(f"   Cleaned to {len(original_mapping)} unique patterns")
    
    print(f"\n=== STEP 3: FIND LARGEST PREFIX PATTERNS ===")
    largest_prefixes = find_largest_prefixes(list(original_mapping.keys()), original_mapping)
    
    print(f"   Found {len(largest_prefixes)} largest prefix patterns:")
    for prefix, objects in largest_prefixes:
        print(f"      '{prefix}': {len(objects)} objects")
    
    print(f"\n=== STEP 4: FIND NUMERIC PATTERNS FOR EACH PREFIX ===")
    final_results = []
    
    for prefix, objects in largest_prefixes:
        print(f"\n   Processing prefix '{prefix}' with {len(objects)} objects:")
        
        # Find numeric patterns within this group
        numeric_patterns = find_numeric_patterns_for_group(list(objects))
        
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

def run_pattern_detection():
    """Main function to run pattern detection on selected objects"""
    
    if not bpy.context.selected_objects:
        print("No objects selected")
        return
    
    # Extract object names
    object_names = [obj.name for obj in bpy.context.selected_objects if obj.name]
    
    if len(object_names) < 2:
        print("Need at least 2 objects to detect patterns")
        return
    
    print(f"\n=== REDESIGNED PATTERN DETECTION ANALYSIS ===")
    print(f"Analyzing {len(object_names)} object names")
    
    # Perform redesigned pattern detection
    final_results = redesigned_pattern_detection(object_names)
    
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

# Run the pattern detection
if __name__ == "__main__":
    run_pattern_detection()

# You can also call this function directly:
# run_pattern_detection()
