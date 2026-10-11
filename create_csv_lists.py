#!/usr/bin/env python3
"""
Create CSV files listing entities and relationships for manual review.
"""

import json
import csv
from pathlib import Path

def create_entities_csv():
    """Create CSV file with entity list."""
    with open('/home/user/pid-book/entities_refined.json') as f:
        entities = json.load(f)

    # Sort by frequency (most frequent first)
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[1]), reverse=True)

    output_file = Path('/home/user/pid-book/entities_list.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['Entity', 'Occurrences', 'Keep'])

        # Write each entity
        for entity, occurrences in sorted_entities:
            writer.writerow([entity, len(occurrences), 'yes'])

    print(f"Created {output_file}")
    print(f"  Total entities: {len(sorted_entities)}")
    return output_file

def create_relationships_csv():
    """Create CSV file with relationship list."""
    with open('/home/user/pid-book/relationships_refined.json') as f:
        relationships = json.load(f)

    # Sort by frequency (most frequent first)
    sorted_rels = sorted(relationships.items(), key=lambda x: len(x[1]), reverse=True)

    output_file = Path('/home/user/pid-book/relationships_list.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['Relationship', 'Instances', 'Example_Source', 'Example_Target', 'Keep'])

        # Write each relationship
        for rel_type, instances in sorted_rels:
            if instances:
                example = instances[0]
                writer.writerow([
                    rel_type,
                    len(instances),
                    example['source'],
                    example['target'],
                    'yes'
                ])
            else:
                writer.writerow([rel_type, 0, '', '', 'yes'])

    print(f"Created {output_file}")
    print(f"  Total relationships: {len(sorted_rels)}")
    return output_file

if __name__ == '__main__':
    print("Creating CSV files for manual review...\n")
    entities_file = create_entities_csv()
    print()
    relationships_file = create_relationships_csv()
    print("\n" + "="*80)
    print("CSV files created successfully!")
    print("="*80)
    print("\nYou can now edit these files to fine-tune your selection:")
    print(f"  1. {entities_file}")
    print(f"  2. {relationships_file}")
    print("\nChange 'yes' to 'no' in the 'Keep' column to exclude items.")
