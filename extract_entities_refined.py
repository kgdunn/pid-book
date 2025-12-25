#!/usr/bin/env python3
"""
Refined entity and relationship extraction for knowledge graphs.
Focuses on domain-specific statistical and DOE concepts.
"""

import spacy
import json
import re
from collections import defaultdict
from pathlib import Path

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Domain-specific terms (expanded list)
DOMAIN_KEYWORDS = {
    'factorial', 'design', 'experiment', 'factor', 'level', 'interaction',
    'blocking', 'confounding', 'randomization', 'replication', 'response',
    'treatment', 'variance', 'effect', 'main effect', 'regression',
    'anova', 'statistical', 'significance', 'hypothesis', 'model',
    'residual', 'coefficient', 'intercept', 'slope', 'optimization',
    'screening', 'resolution', 'generator', 'alias', 'contrast',
    'curvature', 'quadratic', 'linear', 'surface', 'doe', 'ofat',
    'plackett', 'burman', 'central composite', 'box-behnken',
    'fractional', 'full factorial', 'half fraction', 'disturbance',
    'bias', 'error', 'replicate', 'run', 'trial', 'batch',
    'correlation', 'covariance', 'least squares', 'parameter',
    'predictor', 'categorical', 'continuous', 'discrete'
}

# Stopwords to exclude
EXCLUDE_WORDS = {
    'we', 'it', 'they', 'this', 'that', 'these', 'those', 'i', 'you',
    'he', 'she', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'first', 'second', 'third', 'last', 'next',
    'alt', 'width', 'scale', 'align', 'center', 'left', 'right',
    'image', 'figure', 'table', 'px', 'fake', 'http', 'https', 'www',
    'youtube', 'com', 'video', 'math', 'displaystyle'
}

# RST artifacts to exclude (regex patterns)
EXCLUDE_PATTERNS = [
    r'^\d+px$',  # Like 900px
    r'^[a-z]\s*\|',  # Table column markers like "c | ab"
    r'^:\w+:',  # RST directives like :scale:
    r'^\.\.',  # RST comments/directives
    r'math:`',  # Math expressions
    r'^\d+$',  # Pure numbers
    r'^[a-z]$',  # Single letters
]

def is_excluded(text):
    """Check if text should be excluded."""
    text = text.lower().strip()

    # Check exclude list
    if text in EXCLUDE_WORDS:
        return True

    # Check patterns
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, text):
            return True

    # Too short
    if len(text) < 3:
        return True

    return False

def is_domain_relevant(text):
    """Check if text is domain-relevant."""
    text = text.lower().strip()

    # Direct match
    if text in DOMAIN_KEYWORDS:
        return True

    # Contains domain keyword
    for keyword in DOMAIN_KEYWORDS:
        if keyword in text:
            return True
        # Also check if text is part of a multi-word keyword
        if text in keyword.split():
            return True

    return False

def normalize_entity(text):
    """Normalize entity text."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    # Remove trailing punctuation
    text = re.sub(r'[.,;:!?]+$', '', text)
    return text

def extract_entities_refined(text, current_file, start_line):
    """Extract domain-relevant entities with better filtering."""
    entities = defaultdict(list)
    doc = nlp(text)

    seen_in_doc = set()

    # Extract noun chunks
    for chunk in doc.noun_chunks:
        normalized = normalize_entity(chunk.text)

        # Skip if excluded or already seen
        if is_excluded(normalized) or normalized in seen_in_doc:
            continue

        # Only keep if domain-relevant
        if is_domain_relevant(normalized):
            line_offset = text[:chunk.start_char].count('\n')
            entities[normalized].append({
                "file": current_file,
                "line": start_line + line_offset,
                "context": chunk.sent.text.strip()[:150],
                "type": "CONCEPT"
            })
            seen_in_doc.add(normalized)

    # Extract named entities (if domain-relevant)
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART']:  # Skip persons, dates, etc.
            normalized = normalize_entity(ent.text)

            if is_excluded(normalized) or normalized in seen_in_doc:
                continue

            if is_domain_relevant(normalized):
                line_offset = text[:ent.start_char].count('\n')
                entities[normalized].append({
                    "file": current_file,
                    "line": start_line + line_offset,
                    "context": ent.sent.text.strip()[:150],
                    "type": ent.label_
                })
                seen_in_doc.add(normalized)

    return entities

def extract_relationships_refined(text, current_file, start_line, entities_set):
    """Extract relationships with better filtering."""
    relationships = defaultdict(list)
    doc = nlp(text)

    for sent in doc.sents:
        root = sent.root

        if root.pos_ != 'VERB':
            continue

        # Find subjects and objects
        subjects = [child for child in root.children if child.dep_ in ['nsubj', 'nsubjpass']]
        objects = [child for child in root.children if child.dep_ in ['dobj', 'pobj', 'attr']]

        # Add objects from prepositional phrases
        for child in root.children:
            if child.dep_ == 'prep':
                objects.extend([gc for gc in child.children if gc.dep_ == 'pobj'])

        # Create relationships
        for subj in subjects:
            subj_phrase = normalize_entity(' '.join([t.text for t in subj.subtree]))

            # Skip if excluded
            if is_excluded(subj_phrase):
                continue

            for obj in objects:
                obj_phrase = normalize_entity(' '.join([t.text for t in obj.subtree]))

                # Skip if excluded
                if is_excluded(obj_phrase):
                    continue

                # Only keep if both are domain-relevant or in our entities set
                if (is_domain_relevant(subj_phrase) or subj_phrase in entities_set) and \
                   (is_domain_relevant(obj_phrase) or obj_phrase in entities_set):

                    relation = normalize_entity(root.lemma_)
                    line_offset = text[:sent.start_char].count('\n')

                    relationships[relation].append({
                        "source": subj_phrase,
                        "target": obj_phrase,
                        "file": current_file,
                        "line": start_line + line_offset,
                        "context": sent.text.strip()[:150]
                    })

    return relationships

def merge_dict_lists(dict_list):
    """Merge list of dictionaries with list values."""
    merged = defaultdict(list)
    for d in dict_list:
        for key, values in d.items():
            merged[key].extend(values)
    return dict(merged)

def process_text_file(input_file):
    """Process extracted text file."""
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by file markers
    file_sections = re.split(r'={80}\nFILE: (.+?)\n={80}\n', content)

    all_entities = []
    all_relationships = []

    # First pass: extract all entities
    print("\nExtracting entities...")
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        print(f"  Processing {current_file}...")
        entities = extract_entities_refined(text, current_file, start_line=1)
        all_entities.append(entities)

    # Merge entities
    print("\nMerging entities...")
    merged_entities = merge_dict_lists(all_entities)
    entities_set = set(merged_entities.keys())
    print(f"Found {len(merged_entities)} unique entities")

    # Second pass: extract relationships
    print("\nExtracting relationships...")
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        relationships = extract_relationships_refined(text, current_file, start_line=1,
                                                     entities_set=entities_set)
        all_relationships.append(relationships)

    # Merge relationships
    print("Merging relationships...")
    merged_relationships = merge_dict_lists(all_relationships)
    print(f"Found {len(merged_relationships)} unique relationship types")

    return merged_entities, merged_relationships

def main():
    """Main extraction process."""
    input_file = Path('/home/user/pid-book/doe_extracted_text.txt')

    # Extract
    entities, relationships = process_text_file(input_file)

    # Save
    output_entities = Path('/home/user/pid-book/entities_refined.json')
    output_relationships = Path('/home/user/pid-book/relationships_refined.json')

    print(f"\nSaving entities to {output_entities}...")
    with open(output_entities, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)

    print(f"Saving relationships to {output_relationships}...")
    with open(output_relationships, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2, ensure_ascii=False)

    # Statistics
    print("\n" + "="*80)
    print("REFINED EXTRACTION STATISTICS")
    print("="*80)
    print(f"Total unique entities: {len(entities)}")
    print(f"Total entity occurrences: {sum(len(v) for v in entities.values())}")
    print(f"\nTotal unique relationship types: {len(relationships)}")
    print(f"Total relationship instances: {sum(len(v) for v in relationships.values())}")

    # Top entities
    print("\n" + "="*80)
    print("TOP 30 MOST FREQUENT ENTITIES")
    print("="*80)
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[1]), reverse=True)
    for entity, occurrences in sorted_entities[:30]:
        print(f"{entity:50s} ({len(occurrences)} occurrences)")

    # Top relationships
    print("\n" + "="*80)
    print("TOP 20 MOST FREQUENT RELATIONSHIPS")
    print("="*80)
    sorted_relationships = sorted(relationships.items(), key=lambda x: len(x[1]), reverse=True)
    for relation, instances in sorted_relationships[:20]:
        print(f"{relation:40s} ({len(instances)} instances)")
        # Show a sample
        if instances:
            sample = instances[0]
            print(f"    Example: {sample['source']} -> {sample['target']}")

    print("\n" + "="*80)
    print("Refined extraction complete!")
    print("="*80)

if __name__ == '__main__':
    main()
