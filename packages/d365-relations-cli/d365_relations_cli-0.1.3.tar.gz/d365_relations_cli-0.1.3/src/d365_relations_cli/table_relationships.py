#!/usr/bin/env python
import json
import os
from collections import defaultdict, deque
import time

class AdvancedTableRelationshipFinder:
    """
    A class to find relationships between Dynamics 365 tables based on field associations.
    Works with the advanced optimized file format (ID-based) produced by optimize_json.py.
    Provides case-insensitive table name lookups and efficient memory usage.
    """
    
    def __init__(self, json_file_path='tablefieldassociations_opt.json'):
        """
        Initialize the TableRelationshipFinder with the path to the JSON file containing table field associations.
        
        Args:
            json_file_path (str): Path to the advanced optimized JSON file with table field associations
        """
        self.json_file_path = json_file_path
        self.relationships_graph = defaultdict(list)
        self.relationship_details = {}
        self.table_name_map = {}  # Maps lowercase table names to their original case
        self.table_id_map = {}    # Maps table names to their IDs
        self.field_id_map = {}    # Maps field names to their IDs
        self._load_relationships()
    
    def _load_relationships(self):
        """
        Load relationships from the advanced optimized JSON file and create an in-memory representation.
        The file is expected to have the format produced by optimize_json.py.
        """
        start_time = time.time()
        print(f"Loading relationships from {self.json_file_path}...")
        
        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"The file {self.json_file_path} was not found.")
        
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
        
        # Check if this is an advanced optimized file
        if not isinstance(data, dict) or not all(k in data for k in ["tables", "fields", "relationships"]):
            raise ValueError(f"The file {self.json_file_path} is not in the advanced optimized format.")
        
        # Load table and field mappings
        tables = {int(k): v for k, v in data["tables"].items()}
        fields = {int(k): v for k, v in data["fields"].items()}
        relationships = data["relationships"]
        
        # Create reverse mappings
        self.table_id_map = {v: int(k) for k, v in data["tables"].items()}
        self.field_id_map = {v: int(k) for k, v in data["fields"].items()}
        
        # Build the table name mapping for case-insensitive lookups
        for table_name in self.table_id_map.keys():
            self.table_name_map[table_name.lower()] = table_name
        
        # Build the graph representation
        for rel in relationships:
            parent_table_id, parent_field_id, child_table_id, child_field_id = rel
            
            parent_table = tables[parent_table_id]
            parent_field = fields[parent_field_id]
            child_table = tables[child_table_id]
            child_field = fields[child_field_id]
            
            # Add forward relationship
            relationship_key = f"{parent_table}:{child_table}"
            self.relationship_details[relationship_key] = {
                'parent_field': parent_field,
                'child_field': child_field
            }
            if child_table not in self.relationships_graph[parent_table]:
                self.relationships_graph[parent_table].append(child_table)
            
            # Add reverse relationship (always add for completeness, since we've already deduplicated)
            reverse_key = f"{child_table}:{parent_table}"
            if reverse_key not in self.relationship_details:
                self.relationship_details[reverse_key] = {
                    'parent_field': child_field,
                    'child_field': parent_field
                }
                if parent_table not in self.relationships_graph[child_table]:
                    self.relationships_graph[child_table].append(parent_table)
        
        relationship_count = len(relationships)
        load_time = time.time() - start_time
        print(f"Loaded {relationship_count} relationships in {load_time:.2f} seconds.")
        print(f"Graph contains {len(self.relationships_graph)} tables.")
    
    def _get_original_table_name(self, table_name):
        """
        Get the original case of a table name from the case-insensitive lookup.
        
        Args:
            table_name (str): Table name in any case
            
        Returns:
            str: The original case of the table name or the input if not found
        """
        return self.table_name_map.get(table_name.lower(), table_name)
    
    def find_related(self, table):
        """
        Find all tables directly related to the specified table.
        
        Args:
            table (str): Name of the table to find relationships for (case-insensitive)
            
        Returns:
            dict: A dictionary mapping related table names to their relationship fields
        """
        # Convert to original case for lookup
        original_table = self._get_original_table_name(table)
        
        if original_table not in self.relationships_graph:
            return {}
        
        related_tables = {}
        for related_table in self.relationships_graph[original_table]:
            key = f"{original_table}:{related_table}"
            reverse_key = f"{related_table}:{original_table}"
            
            # Check if we have details for this relationship
            if key in self.relationship_details:
                details = self.relationship_details[key]
                related_tables[related_table] = {
                    'source_field': details['parent_field'],
                    'target_field': details['child_field'],
                    'relationship_type': 'parent-to-child'
                }
            elif reverse_key in self.relationship_details:
                details = self.relationship_details[reverse_key]
                related_tables[related_table] = {
                    'source_field': details['child_field'],
                    'target_field': details['parent_field'],
                    'relationship_type': 'child-to-parent'
                }
        
        return related_tables
    
    def find_relationship(self, table1, table2, levels=0):
        """
        Find paths between two tables through their relationships.
        
        Args:
            table1 (str): Name of the first table (case-insensitive)
            table2 (str): Name of the second table (case-insensitive)
            levels (int): Maximum number of intermediate tables to check
            
        Returns:
            list: A list of paths, where each path is a list of (table, field, relationship_type) tuples
        """
        # Convert to original case for lookup
        original_table1 = self._get_original_table_name(table1)
        original_table2 = self._get_original_table_name(table2)
        
        if original_table1 not in self.relationships_graph or original_table2 not in self.relationships_graph:
            return []
        
        if original_table1 == original_table2:
            return [[original_table1]]
        
        # Use BFS to find all paths within the specified levels
        queue = deque([(original_table1, [original_table1], 0)])
        visited = set([original_table1])  # Track visited tables to avoid cycles
        all_paths = []
        
        while queue:
            current_table, path, current_level = queue.popleft()
            
            # If we've reached the maximum level, don't explore further
            if current_level > levels:
                continue
            
            # Check each neighbor
            for neighbor in self.relationships_graph[current_table]:
                # If we've found the target table, add the path
                if neighbor == original_table2:
                    new_path = path + [neighbor]
                    all_paths.append(new_path)
                    continue
                
                # If we haven't visited this table yet and haven't reached the max level
                if neighbor not in path and current_level < levels:
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path, current_level + 1))
        
        # Enrich paths with field information
        enriched_paths = []
        for path in all_paths:
            enriched_path = []
            for i in range(len(path) - 1):
                source_table = path[i]
                target_table = path[i + 1]
                
                # Check both directions of the relationship
                forward_key = f"{source_table}:{target_table}"
                reverse_key = f"{target_table}:{source_table}"
                
                if forward_key in self.relationship_details:
                    details = self.relationship_details[forward_key]
                    enriched_path.append((source_table, details['parent_field'], 'parent'))
                    if i == len(path) - 2:  # Add the last table in the path
                        enriched_path.append((target_table, details['child_field'], 'child'))
                
                elif reverse_key in self.relationship_details:
                    details = self.relationship_details[reverse_key]
                    enriched_path.append((source_table, details['child_field'], 'child'))
                    if i == len(path) - 2:  # Add the last table in the path
                        enriched_path.append((target_table, details['parent_field'], 'parent'))
            
            if enriched_path:  # Only add paths that have relationship details
                enriched_paths.append(enriched_path)
        
        # Sort paths by length (shortest first)
        return sorted(enriched_paths, key=len)

    def get_table_list(self):
        """
        Get a list of all tables in the dataset.
        
        Returns:
            list: A list of all table names
        """
        return list(self.relationships_graph.keys())

    def get_stats(self):
        """
        Get statistics about the loaded relationships.
        
        Returns:
            dict: A dictionary with statistics
        """
        table_count = len(self.relationships_graph)
        relationship_count = sum(len(relations) for relations in self.relationships_graph.values()) // 2
        
        return {
            'table_count': table_count,
            'unique_fields': len(self.field_id_map),
            'relationship_count': relationship_count,
            'advanced_optimization': "Using ID-based format for maximum compression",
            'case_insensitive': "Table names can be looked up in any case."
        }
    
    def get_relationship_details(self, table1, table2):
        """
        Get detailed information about the relationship between two tables.
        
        Args:
            table1 (str): Name of the first table (case-insensitive)
            table2 (str): Name of the second table (case-insensitive)
            
        Returns:
            dict: A dictionary with relationship details, or None if no direct relationship exists
        """
        # Convert to original case for lookup
        original_table1 = self._get_original_table_name(table1)
        original_table2 = self._get_original_table_name(table2)
        
        forward_key = f"{original_table1}:{original_table2}"
        reverse_key = f"{original_table2}:{original_table1}"
        
        if forward_key in self.relationship_details:
            details = self.relationship_details[forward_key]
            return {
                'source_table': original_table1,
                'source_field': details['parent_field'],
                'target_table': original_table2,
                'target_field': details['child_field'],
                'relationship_type': 'parent-to-child'
            }
        elif reverse_key in self.relationship_details:
            details = self.relationship_details[reverse_key]
            return {
                'source_table': original_table1,
                'source_field': details['child_field'],
                'target_table': original_table2,
                'target_field': details['parent_field'],
                'relationship_type': 'child-to-parent'
            }
        
        return None 