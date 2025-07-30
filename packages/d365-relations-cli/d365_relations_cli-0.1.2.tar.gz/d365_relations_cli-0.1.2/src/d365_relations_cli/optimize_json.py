#!/usr/bin/env python
"""
Advanced utility script to optimize tablefieldassociations.json by:
1. Removing duplicate bi-directional relationships
2. Using numeric IDs for tables and fields instead of repeating strings
3. Creating lookup dictionaries for table and field names
This significantly reduces file size while maintaining all necessary relationship information.

Optimizes the file from https://raw.githubusercontent.com/ameyer505/MicrosoftDynamicsTableAssociations/refs/heads/master/tablefieldassociations.json
"""
import json
import os
import time
import sys

def optimize_relationship_file(input_file_path, output_file_path):
    """
    Advanced optimization of a table relationship JSON file.
    
    Args:
        input_file_path (str): Path to the original JSON file
        output_file_path (str): Path to save the optimized JSON file
    
    Returns:
        dict: Statistics about the optimization process
    """
    start_time = time.time()
    print(f"Reading original file from {input_file_path}...")
    
    # Check if input file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    
    # Read the original file
    with open(input_file_path, 'r') as f:
        original_data = json.load(f)
    
    original_count = len(original_data)
    original_size = os.path.getsize(input_file_path)
    print(f"Original file contains {original_count} relationships and is {original_size/1024/1024:.2f} MB.")
    
    # Step 1: Create lookup dictionaries for tables and fields
    table_to_id = {}
    field_to_id = {}
    next_table_id = 0
    next_field_id = 0
    
    print("Building table and field dictionaries...")
    
    for relationship in original_data:
        parent_table = relationship['ParentTableName']
        parent_field = relationship['ParentFieldName']
        child_table = relationship['ChildTableName']
        child_field = relationship['ChildFieldName']
        
        # Assign IDs to tables
        if parent_table not in table_to_id:
            table_to_id[parent_table] = next_table_id
            next_table_id += 1
        
        if child_table not in table_to_id:
            table_to_id[child_table] = next_table_id
            next_table_id += 1
        
        # Assign IDs to fields
        if parent_field not in field_to_id:
            field_to_id[parent_field] = next_field_id
            next_field_id += 1
        
        if child_field not in field_to_id:
            field_to_id[child_field] = next_field_id
            next_field_id += 1
    
    # Create reverse lookup dictionaries
    id_to_table = {v: k for k, v in table_to_id.items()}
    id_to_field = {v: k for k, v in field_to_id.items()}
    
    # Step 2: Remove duplicate relationships and convert to ID-based format
    processed_relationships = set()
    optimized_relationships = []
    
    print("Converting to optimized format and removing duplicates...")
    
    for relationship in original_data:
        parent_table = relationship['ParentTableName']
        parent_field = relationship['ParentFieldName']
        child_table = relationship['ChildTableName']
        child_field = relationship['ChildFieldName']
        
        # Get IDs
        parent_table_id = table_to_id[parent_table]
        parent_field_id = field_to_id[parent_field]
        child_table_id = table_to_id[child_table]
        child_field_id = field_to_id[child_field]
        
        # Create a canonical representation to check for duplicates
        if parent_table.lower() <= child_table.lower():
            rel_key = f"{parent_table_id}:{parent_field_id}:{child_table_id}:{child_field_id}"
            rel_data = [parent_table_id, parent_field_id, child_table_id, child_field_id]
        else:
            rel_key = f"{child_table_id}:{child_field_id}:{parent_table_id}:{parent_field_id}"
            # Don't switch the actual data order - we'll keep original direction
            rel_data = [parent_table_id, parent_field_id, child_table_id, child_field_id]
        
        # Only add this relationship if we haven't seen it before
        if rel_key not in processed_relationships:
            processed_relationships.add(rel_key)
            optimized_relationships.append(rel_data)
    
    # Create the optimized data structure
    optimized_data = {
        "tables": id_to_table,
        "fields": id_to_field,
        "relationships": optimized_relationships
    }
    
    # Write the optimized data to the output file
    print(f"Writing optimized file to {output_file_path}...")
    with open(output_file_path, 'w') as f:
        json.dump(optimized_data, f, separators=(',', ':'))  # Use compact format
    
    optimized_count = len(optimized_relationships)
    optimized_size = os.path.getsize(output_file_path)
    
    # Calculate statistics
    stats = {
        'original_relationships': original_count,
        'optimized_relationships': optimized_count,
        'relationships_removed': original_count - optimized_count,
        'tables_count': len(table_to_id),
        'fields_count': len(field_to_id),
        'original_size_mb': original_size / 1024 / 1024,
        'optimized_size_mb': optimized_size / 1024 / 1024,
        'size_reduction_percent': (1 - (optimized_size / original_size)) * 100,
        'processing_time_seconds': time.time() - start_time
    }
    
    # Print summary
    print("\nAdvanced Optimization complete!")
    print(f"Original relationships: {stats['original_relationships']}")
    print(f"Optimized relationships: {stats['optimized_relationships']}")
    print(f"Relationships removed: {stats['relationships_removed']}")
    print(f"Unique tables: {stats['tables_count']}")
    print(f"Unique fields: {stats['fields_count']}")
    print(f"Original file size: {stats['original_size_mb']:.2f} MB")
    print(f"Optimized file size: {stats['optimized_size_mb']:.2f} MB")
    print(f"Size reduction: {stats['size_reduction_percent']:.2f}%")
    print(f"Processing time: {stats['processing_time_seconds']:.2f} seconds")
    
    return stats 