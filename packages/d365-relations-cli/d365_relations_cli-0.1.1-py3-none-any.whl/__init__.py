"""
Dynamics 365 Table Relationship Finder

A package for finding relationships between Dynamics 365 tables.
"""

__version__ = '0.1.0'

from .table_relationships import AdvancedTableRelationshipFinder
from .optimize_json import optimize_relationship_file

__all__ = ['AdvancedTableRelationshipFinder', 'optimize_relationship_file'] 