#!/usr/bin/env python3
"""
Extract relationships including variants and abbreviations for knowledge graphs.
"""

import spacy
import json
import re
from collections import defaultdict
from pathlib import Path

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Define variant relationships
VARIANT_RELATIONSHIPS = [
    {"variant": "two-way ANOVA", "canonical": "ANOVA", "type": "IS_VARIANT_OF"},
    {"variant": "one-way ANOVA", "canonical": "ANOVA", "type": "IS_VARIANT_OF"},
    {"variant": "two-factor ANOVA", "canonical": "ANOVA", "type": "IS_VARIANT_OF"},
    {"variant": "two-factor interaction", "canonical": "interaction", "type": "IS_VARIANT_OF"},
    {"variant": "three-factor interaction", "canonical": "interaction", "type": "IS_VARIANT_OF"},
    {"variant": "half-fraction design", "canonical": "fractional factorial design", "type": "IS_VARIANT_OF"},
    {"variant": "screening design", "canonical": "DOE", "type": "IS_VARIANT_OF"},
    {"variant": "foldover design", "canonical": "fractional factorial design", "type": "IS_VARIANT_OF"},
]

# Define abbreviation relationships
ABBREVIATION_RELATIONSHIPS = [
    {"abbreviation": "DOE", "full_form": "design of experiments", "type": "ABBREVIATION_OF"},
    {"abbreviation": "ANOVA", "full_form": "analysis of variance", "type": "ABBREVIATION_OF"},
    {"abbreviation": "CCD", "full_form": "central composite design", "type": "ABBREVIATION_OF"},
    {"abbreviation": "RSM", "full_form": "response surface methodology", "type": "ABBREVIATION_OF"},
    {"abbreviation": "OFAT", "full_form": "one-variable-at-a-time", "type": "ABBREVIATION_OF"},
    {"abbreviation": "COST", "full_form": "change one single variable at a time", "type": "ABBREVIATION_OF"},
    {"abbreviation": "2FI", "full_form": "two-factor interaction", "type": "ABBREVIATION_OF"},
    {"abbreviation": "3FI", "full_form": "three-factor interaction", "type": "ABBREVIATION_OF"},
]

# Canonical entity mappings (from previous script)
CANONICAL_ENTITIES = {
    'main effect', 'experiment', 'factor', 'DOE', 'response variable',
    'interaction', 'least squares model', 'full factorial design',
    'fractional factorial design', 'half-fraction design', 'defining relationship',
    'standard error', 'intercept', 'response surface methodology', 'curvature',
    'steepest ascent', 'linear model', 'disturbance', 'design resolution',
    'projectivity', 'variance', 'coefficient', 'two-factor interaction',
    'blocking', 'three-factor interaction', 'aliasing', 'experimental run',
    'optimization', 'confounding pattern', 'confidence interval',
    'central composite design', 'ANOVA', 'confounding', 'randomization',
    'replication', 'quadratic model', 'regression', 'treatment', 'level',
    't-test', 'F-test', 'p-value', 'statistical significance', 'screening design',
    'generator', 'contrast', 'residual', 'error', 'slope', 'trial',
    'observation', 'bias', 'OFAT', 'COST', 'Plackett-Burman design',
    'Box-Behnken design', 'Latin square design', 'null hypothesis',
    'alternative hypothesis', 'Type I error', 'Type II error', 'alpha',
    'beta', 'statistical power', 'regression model', 'steepest descent',
    'foldover design', 'hypothesis test'
}

def extract_semantic_relationships(text, current_file, start_line):
    """Extract semantic relationships from text."""
    relationships = []
    doc = nlp(text)

    # Common relationship verbs for DOE concepts
    relationship_verbs = {
        'affect': 'AFFECTS',
        'influence': 'INFLUENCES',
        'determine': 'DETERMINES',
        'estimate': 'ESTIMATES',
        'calculate': 'CALCULATES',
        'measure': 'MEASURES',
        'confound': 'CONFOUNDS',
        'alias': 'ALIASES',
        'block': 'BLOCKS',
        'require': 'REQUIRES',
        'use': 'USES',
        'analyze': 'ANALYZES',
        'optimize': 'OPTIMIZES',
        'minimize': 'MINIMIZES',
        'maximize': 'MAXIMIZES',
    }

    for sent in doc.sents:
        root = sent.root

        if root.lemma_ in relationship_verbs:
            # Find subjects and objects
            subjects = [child for child in root.children if child.dep_ in ['nsubj', 'nsubjpass']]
            objects = [child for child in root.children if child.dep_ in ['dobj', 'pobj', 'attr']]

            # Add prep objects
            for child in root.children:
                if child.dep_ == 'prep':
                    objects.extend([gc for gc in child.children if gc.dep_ == 'pobj'])

            for subj in subjects:
                subj_text = ' '.join([t.text for t in subj.subtree]).lower().strip()

                for obj in objects:
                    obj_text = ' '.join([t.text for t in obj.subtree]).lower().strip()

                    # Only create relationship if both are canonical entities
                    if subj_text in CANONICAL_ENTITIES and obj_text in CANONICAL_ENTITIES:
                        line_offset = text[:sent.start_char].count('\n')

                        relationships.append({
                            "source": subj_text,
                            "relationship": relationship_verbs[root.lemma_],
                            "target": obj_text,
                            "context": sent.text.strip()[:150],
                            "confidence": 0.75,
                            "file": current_file,
                            "line": start_line + line_offset
                        })

    return relationships

def process_text_for_relationships(input_file):
    """Process text file to extract relationships."""
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by file markers
    file_sections = re.split(r'={80}\nFILE: (.+?)\n={80}\n', content)

    all_relationships = []

    # Extract relationships from each section
    print("\nExtracting semantic relationships...")
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        print(f"  Processing {current_file}...")
        relationships = extract_semantic_relationships(text, current_file, start_line=1)
        all_relationships.extend(relationships)

    return all_relationships

def create_structural_relationships():
    """Create structural relationships (variants and abbreviations)."""
    relationships = []

    # Add variant relationships
    for variant_rel in VARIANT_RELATIONSHIPS:
        relationships.append({
            "source": variant_rel["variant"],
            "relationship": variant_rel["type"],
            "target": variant_rel["canonical"],
            "context": f"{variant_rel['variant']} is a variant of {variant_rel['canonical']}",
            "confidence": 1.0,
            "file": "structural",
            "line": 0
        })

    # Add abbreviation relationships
    for abbr_rel in ABBREVIATION_RELATIONSHIPS:
        relationships.append({
            "source": abbr_rel["abbreviation"],
            "relationship": abbr_rel["type"],
            "target": abbr_rel["full_form"],
            "context": f"{abbr_rel['abbreviation']} is an abbreviation of {abbr_rel['full_form']}",
            "confidence": 1.0,
            "file": "structural",
            "line": 0
        })

    return relationships

def main():
    """Main extraction process."""
    input_file = Path('/home/user/pid-book/doe_extracted_text.txt')

    # Extract semantic relationships
    semantic_relationships = process_text_for_relationships(input_file)

    # Create structural relationships
    structural_relationships = create_structural_relationships()

    # Combine all relationships
    all_relationships = semantic_relationships + structural_relationships

    # Save as JSON array
    output_file = Path('/home/user/pid-book/relationships_canonical.json')

    print(f"\nSaving relationships to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_relationships, f, indent=2, ensure_ascii=False)

    # Statistics
    print("\n" + "="*80)
    print("RELATIONSHIP EXTRACTION STATISTICS")
    print("="*80)
    print(f"Total relationships: {len(all_relationships)}")
    print(f"  Semantic relationships: {len(semantic_relationships)}")
    print(f"  Structural relationships: {len(structural_relationships)}")

    # Count by type
    from collections import Counter
    rel_types = Counter(r['relationship'] for r in all_relationships)

    print("\n" + "="*80)
    print("RELATIONSHIPS BY TYPE")
    print("="*80)
    for rel_type, count in rel_types.most_common():
        print(f"{rel_type:30s} ({count} instances)")

    # Show samples
    print("\n" + "="*80)
    print("SAMPLE RELATIONSHIPS")
    print("="*80)

    # Show variant relationships
    print("\nIS_VARIANT_OF relationships:")
    for rel in all_relationships[:5]:
        if rel['relationship'] == 'IS_VARIANT_OF':
            print(f"  {rel['source']} --> {rel['target']}")

    # Show abbreviation relationships
    print("\nABBREVIATION_OF relationships:")
    for rel in all_relationships:
        if rel['relationship'] == 'ABBREVIATION_OF':
            print(f"  {rel['source']} --> {rel['target']}")

    # Show semantic relationships
    print("\nSemantic relationships (sample):")
    semantic_sample = [r for r in semantic_relationships if r['confidence'] >= 0.75][:5]
    for rel in semantic_sample:
        print(f"  {rel['source']} --[{rel['relationship']}]--> {rel['target']}")

    print("\n" + "="*80)
    print("Extraction complete!")
    print("="*80)

if __name__ == '__main__':
    main()
