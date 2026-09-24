#!/usr/bin/env python3
"""
Extract entities and relationships from DOE text for knowledge graph creation.

Output format:
- entities: {entity_name: [{"file": filename, "line": line_num, "context": text}, ...]}
- relationships: {relation_type: [{"source": src, "target": tgt, "file": filename, "line": line_num}, ...]}
"""

import spacy
import json
import re
from collections import defaultdict
from pathlib import Path

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Domain-specific terms for DOE/statistics
DOMAIN_TERMS = {
    'factorial design', 'full factorial', 'fractional factorial', 'blocking',
    'confounding', 'randomization', 'replication', 'response variable',
    'factor', 'level', 'interaction', 'main effect', 'two-factor interaction',
    'three-factor interaction', 'least squares', 'regression', 'anova',
    'variance', 'standard deviation', 'residual', 'p-value', 'significance',
    'confidence interval', 'hypothesis test', 'null hypothesis',
    'alternative hypothesis', 'statistical power', 'type i error', 'type ii error',
    'experimental design', 'treatment', 'control', 'placebo', 'bias',
    'screening design', 'response surface', 'central composite design',
    'box-behnken design', 'plackett-burman design', 'latin square',
    'batch', 'run', 'experiment', 'trial', 'observation', 'sample',
    'population', 'mean', 'median', 'mode', 'range', 'quartile',
    'outlier', 'correlation', 'covariance', 'linear model', 'quadratic model',
    'curvature', 'steepest ascent', 'optimization', 'robustness',
    'doe', 'ofat', 'generator', 'defining relationship', 'alias',
    'resolution', 'foldover', 'projectivity', 'confounding pattern',
    'contrast', 'effect estimate', 'coefficient', 'intercept', 'slope'
}

def normalize_entity(text):
    """Normalize entity text for consistent naming."""
    # Convert to lowercase
    text = text.lower().strip()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def is_relevant_entity(span, doc):
    """Determine if a span is a relevant entity for the knowledge graph."""
    text = normalize_entity(span.text)

    # Check if it's a domain-specific term
    if text in DOMAIN_TERMS:
        return True

    # Check for multi-word domain terms (partial matches)
    for term in DOMAIN_TERMS:
        if term in text or text in term:
            return True

    # Accept noun chunks that are not too long and not stopwords
    if span.root.pos_ in ['NOUN', 'PROPN']:
        # Skip single-character or very short entities
        if len(text) < 3:
            return False
        # Skip common stopwords
        if span.root.is_stop:
            return False
        # Skip pure numbers
        if text.isdigit():
            return False
        return True

    return False

def extract_entities_from_text(text, current_file, start_line):
    """Extract entities from text with metadata."""
    entities = defaultdict(list)

    # Process text with spaCy
    doc = nlp(text)

    # Extract noun chunks and named entities
    seen_in_doc = set()

    # Named entities
    for ent in doc.ents:
        if is_relevant_entity(ent, doc):
            normalized = normalize_entity(ent.text)
            if normalized not in seen_in_doc:
                # Estimate line number (approximate based on character position)
                line_offset = text[:ent.start_char].count('\n')
                entities[normalized].append({
                    "file": current_file,
                    "line": start_line + line_offset,
                    "context": ent.sent.text.strip()[:200],  # First 200 chars of sentence
                    "type": ent.label_
                })
                seen_in_doc.add(normalized)

    # Noun chunks (important concepts)
    for chunk in doc.noun_chunks:
        if is_relevant_entity(chunk, doc):
            normalized = normalize_entity(chunk.text)
            if normalized not in seen_in_doc:
                line_offset = text[:chunk.start_char].count('\n')
                entities[normalized].append({
                    "file": current_file,
                    "line": start_line + line_offset,
                    "context": chunk.sent.text.strip()[:200],
                    "type": "CONCEPT"
                })
                seen_in_doc.add(normalized)

    return entities

def extract_relationships_from_text(text, current_file, start_line, entities_set):
    """Extract relationships (subject-verb-object triples) from text."""
    relationships = defaultdict(list)

    doc = nlp(text)

    for sent in doc.sents:
        # Find root verb
        root = sent.root

        if root.pos_ == 'VERB':
            # Find subject
            subjects = [child for child in root.children if child.dep_ in ['nsubj', 'nsubjpass']]
            # Find objects
            objects = [child for child in root.children if child.dep_ in ['dobj', 'pobj', 'attr', 'dative']]

            # Also check for prep phrases
            for child in root.children:
                if child.dep_ == 'prep':
                    objects.extend([grandchild for grandchild in child.children
                                  if grandchild.dep_ == 'pobj'])

            # Create relationships
            for subj in subjects:
                # Get full noun phrase for subject
                subj_phrase = normalize_entity(' '.join([t.text for t in subj.subtree]))

                for obj in objects:
                    # Get full noun phrase for object
                    obj_phrase = normalize_entity(' '.join([t.text for t in obj.subtree]))

                    # Only create relationship if both entities are in our entities set
                    # or are domain-relevant
                    if (subj_phrase in entities_set or any(term in subj_phrase for term in DOMAIN_TERMS)) and \
                       (obj_phrase in entities_set or any(term in obj_phrase for term in DOMAIN_TERMS)):

                        relation = normalize_entity(root.lemma_)
                        line_offset = text[:sent.start_char].count('\n')

                        relationships[relation].append({
                            "source": subj_phrase,
                            "target": obj_phrase,
                            "file": current_file,
                            "line": start_line + line_offset,
                            "context": sent.text.strip()[:200]
                        })

    return relationships

def merge_entities(entities_list):
    """Merge entities from multiple extractions."""
    merged = defaultdict(list)
    for entities in entities_list:
        for entity, occurrences in entities.items():
            merged[entity].extend(occurrences)
    return dict(merged)

def merge_relationships(relationships_list):
    """Merge relationships from multiple extractions."""
    merged = defaultdict(list)
    for relationships in relationships_list:
        for relation, occurrences in relationships.items():
            merged[relation].extend(occurrences)
    return dict(merged)

def process_extracted_text(input_file):
    """Process the extracted DOE text file."""
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by file markers
    file_sections = re.split(r'={80}\nFILE: (.+?)\n={80}\n', content)

    all_entities = []
    all_relationships = []

    # Process each file section
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        print(f"Processing {current_file}...")

        # Extract entities
        entities = extract_entities_from_text(text, current_file, start_line=1)
        all_entities.append(entities)

    # Merge all entities first
    print("\nMerging entities...")
    merged_entities = merge_entities(all_entities)
    entities_set = set(merged_entities.keys())

    print(f"Found {len(merged_entities)} unique entities")

    # Now extract relationships with knowledge of all entities
    print("\nExtracting relationships...")
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        relationships = extract_relationships_from_text(text, current_file, start_line=1,
                                                       entities_set=entities_set)
        all_relationships.append(relationships)

    # Merge relationships
    print("Merging relationships...")
    merged_relationships = merge_relationships(all_relationships)
    print(f"Found {len(merged_relationships)} unique relationship types")

    return merged_entities, merged_relationships

def main():
    """Main extraction process."""
    input_file = Path('/home/user/pid-book/doe_extracted_text.txt')

    # Extract entities and relationships
    entities, relationships = process_extracted_text(input_file)

    # Save results
    output_entities = Path('/home/user/pid-book/entities.json')
    output_relationships = Path('/home/user/pid-book/relationships.json')

    print(f"\nSaving entities to {output_entities}...")
    with open(output_entities, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)

    print(f"Saving relationships to {output_relationships}...")
    with open(output_relationships, 'w', encoding='utf-8') as f:
        json.dump(relationships, f, indent=2, ensure_ascii=False)

    # Print statistics
    print("\n" + "="*80)
    print("EXTRACTION STATISTICS")
    print("="*80)
    print(f"Total unique entities: {len(entities)}")
    print(f"Total entity occurrences: {sum(len(v) for v in entities.values())}")
    print(f"\nTotal unique relationship types: {len(relationships)}")
    print(f"Total relationship instances: {sum(len(v) for v in relationships.values())}")

    # Show top entities
    print("\n" + "="*80)
    print("TOP 20 MOST FREQUENT ENTITIES")
    print("="*80)
    sorted_entities = sorted(entities.items(), key=lambda x: len(x[1]), reverse=True)
    for entity, occurrences in sorted_entities[:20]:
        print(f"{entity:40s} ({len(occurrences)} occurrences)")

    # Show top relationships
    print("\n" + "="*80)
    print("TOP 20 MOST FREQUENT RELATIONSHIPS")
    print("="*80)
    sorted_relationships = sorted(relationships.items(), key=lambda x: len(x[1]), reverse=True)
    for relation, instances in sorted_relationships[:20]:
        print(f"{relation:40s} ({len(instances)} instances)")

    print("\n" + "="*80)
    print("Files saved successfully!")
    print("="*80)

if __name__ == '__main__':
    main()
