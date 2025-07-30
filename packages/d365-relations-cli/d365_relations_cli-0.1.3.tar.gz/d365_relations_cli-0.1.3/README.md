# Dynamics 365 Table Relationship Finder

A tool for finding relationships between Dynamics 365 tables based on their field associations. This tool efficiently identifies direct and indirect relationships, enabling better understanding of data models.

## Features

- **Find Direct Relationships**: Quickly find all tables directly related to a specific table.
- **Find Relationship Paths**: Discover paths between two tables through their relationships, with control over search depth.
- **Memory Efficient**: Designed to handle large relationship datasets efficiently.
- **Command-line Interface**: Easy-to-use CLI for quick access to relationship information.
- **Case-Insensitive Lookups**: Table names can be specified in any case (uppercase, lowercase, mixed case).

## Installation

```bash
pip install d365-relations-cli
```

## Optimizing the Relationship File

You need to create an advanced optimized version of the `tablefieldassociations.json` file before using the tool. This significantly reduces file size and improves performance:

```bash
# Using the CLI
tr optimize -i tablefieldassociations.json -o tablefieldassociations_opt.json
```

The advanced optimization performs the following:
1. Removes duplicate bi-directional relationships
2. Uses numeric IDs for tables and fields instead of repeating strings
3. Creates lookup dictionaries for table and field names

## Command-line Usage

```bash
# Find all tables directly related to a specific table (case-insensitive)
tr find-related companyinfo

# Find direct relationships between two tables (with no intermediate tables)
tr find-relationship table1 TABLE2

# Find relationships with intermediate tables (specify max number of intermediate tables)
tr find-relationship table1 TABLE2 --levels 2

# Get detailed information about the direct relationship between two tables
tr get-relationship-details Table1 table2

# List all tables in the dataset
tr list-tables

# Show statistics about the loaded relationships
tr stats

# Specify a different optimized JSON file
tr -f custom_tablefieldassociations_opt.json find-related companyinfo

# Save results to a file
tr find-related companyinfo --output results.json
```

### CLI Commands

- `find-related`: Find all tables directly related to a specific table
- `find-relationship`: Find paths between two tables (default is direct relationships only, use --levels to include intermediate tables)
- `get-relationship-details`: Get detailed information about the direct relationship between two tables
- `list-tables`: List all tables in the dataset
- `stats`: Show statistics about the loaded relationships
- `optimize`: Create an advanced optimized version of the relationships file

Run `dynamics365-finder --help` for more information about the available commands and options.

## Python API Usage

```python
from dynamics365_relationship_finder import AdvancedTableRelationshipFinder

# Initialize the finder with the path to your advanced optimized JSON file
finder = AdvancedTableRelationshipFinder('tablefieldassociations_opt.json')

# Find all tables directly related to a specific table (case-insensitive)
related_tables = finder.find_related('Customer')
print(related_tables)

# Find paths between two tables (with no intermediate tables by default)
paths = finder.find_relationship('Customer', 'SalesTable')
print(paths)

# Find paths with up to 2 intermediate tables
paths = finder.find_relationship('Customer', 'SalesTable', levels=2)
print(paths)

# Get detailed information about the direct relationship between two tables
details = finder.get_relationship_details('Customer', 'SalesTable')
print(details)

# List all tables in the dataset
tables = finder.get_table_list()
print(tables)

# Get statistics about the loaded relationships
stats = finder.get_stats()
print(stats)
```

## License

MIT 