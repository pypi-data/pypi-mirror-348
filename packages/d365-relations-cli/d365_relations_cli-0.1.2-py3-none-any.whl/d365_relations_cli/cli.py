#!/usr/bin/env python
import argparse
import json
import os
from d365_relations_cli.table_relationships import AdvancedTableRelationshipFinder
from d365_relations_cli.optimize_json import optimize_relationship_file

def main():
    """
    Command-line interface for the Dynamics 365 Table Relationship Finder.
    Works exclusively with the advanced optimized JSON format.
    """
    parser = argparse.ArgumentParser(
        description='Find relationships between Dynamics 365 tables. Uses the advanced optimized format exclusively.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Add file option
    parser.add_argument(
        '-f', '--file',
        default='tablefieldassociations_opt.json',
        help='Path to the advanced optimized relationships file (default: tablefieldassociations_opt.json).'
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # find-related command
    related_parser = subparsers.add_parser(
        'find-related',
        help='Find all tables directly related to a specific table (case-insensitive)'
    )
    related_parser.add_argument('table', help='Name of the table to find relationships for (case-insensitive)')
    related_parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output file to save results (JSON format)'
    )
    
    # find-relationship command
    relationship_parser = subparsers.add_parser(
        'find-relationship',
        help='Find paths between two tables through their relationships (case-insensitive)'
    )
    relationship_parser.add_argument('table1', help='Name of the first table (case-insensitive)')
    relationship_parser.add_argument('table2', help='Name of the second table (case-insensitive)')
    relationship_parser.add_argument(
        '-l', '--levels',
        type=int,
        default=0,
        help='Maximum number of intermediate tables to check (default: 0)'
    )
    relationship_parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output file to save results (JSON format)'
    )
    
    # get-relationship-details command
    details_parser = subparsers.add_parser(
        'get-relationship-details',
        help='Get detailed information about the relationship between two tables (case-insensitive)'
    )
    details_parser.add_argument('table1', help='Name of the first table (case-insensitive)')
    details_parser.add_argument('table2', help='Name of the second table (case-insensitive)')
    details_parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output file to save results (JSON format)'
    )
    
    # list-tables command
    list_parser = subparsers.add_parser(
        'list-tables',
        help='List all tables in the dataset'
    )
    list_parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output file to save results (JSON format)'
    )
    
    # stats command
    stats_parser = subparsers.add_parser(
        'stats',
        help='Show statistics about the loaded relationships'
    )
    
    # optimize command
    optimize_parser = subparsers.add_parser(
        'optimize',
        help='Create an advanced optimized version of the relationships file'
    )
    optimize_parser.add_argument(
        '-i', '--input',
        default='tablefieldassociations.json',
        help='Path to the original JSON file (default: tablefieldassociations.json)'
    )
    optimize_parser.add_argument(
        '-o', '--output',
        default='tablefieldassociations_opt.json',
        help='Path to save the advanced optimized JSON file (default: tablefieldassociations_opt.json)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        return
    
    # Handle optimize command separately
    if args.command == 'optimize':
        try:
            optimize_relationship_file(args.input, args.output)
        except Exception as e:
            print(f"Error during optimization: {e}")
        return
    
    # Initialize the finder
    try:
        finder = AdvancedTableRelationshipFinder(args.file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {args.file}")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Execute the appropriate command
    if args.command == 'find-related':
        result = finder.find_related(args.table)
        if not result:
            print(f"No relationships found for table '{args.table}'. Check if the table name is correct.")
        else:
            print(f"\nTables related to {args.table}:")
            for table, fields in result.items():
                rel_type = fields.get('relationship_type', 'unknown')
                print(f"  {table}: {fields['source_field']} -> {fields['target_field']} ({rel_type})")
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to {args.output}")
    
    elif args.command == 'find-relationship':
        paths = finder.find_relationship(args.table1, args.table2, args.levels)
        if not paths:
            print(f"No relationship found between '{args.table1}' and '{args.table2}' within {args.levels} levels.")
        else:
            print(f"\nRelationship between {args.table1} and {args.table2}:")
            for i, path in enumerate(paths, 1):
                print(f"Path {i}:")
                for table, field, rel_type in path:
                    print(f"  {table}.{field} ({rel_type})")
            
            # Save to file if requested
            if args.output:
                # Convert tuples to lists for JSON serialization
                serializable_paths = []
                for path in paths:
                    serializable_paths.append([{"table": t, "field": f, "relationship_type": rt} for t, f, rt in path])
                
                with open(args.output, 'w') as f:
                    json.dump(serializable_paths, f, indent=2)
                print(f"\nResults saved to {args.output}")
    
    elif args.command == 'get-relationship-details':
        details = finder.get_relationship_details(args.table1, args.table2)
        if not details:
            print(f"No direct relationship found between '{args.table1}' and '{args.table2}'.")
        else:
            print(f"\nRelationship details between {args.table1} and {args.table2}:")
            print(f"  Type: {details['relationship_type']}")
            print(f"  Source: {details['source_table']}.{details['source_field']}")
            print(f"  Target: {details['target_table']}.{details['target_field']}")
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(details, f, indent=2)
                print(f"\nResults saved to {args.output}")
    
    elif args.command == 'list-tables':
        tables = finder.get_table_list()
        print(f"\nFound {len(tables)} tables:")
        for table in sorted(tables):
            print(f"  {table}")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(sorted(tables), f, indent=2)
            print(f"\nResults saved to {args.output}")
    
    elif args.command == 'stats':
        stats = finder.get_stats()
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 