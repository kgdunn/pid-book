#!/usr/bin/env python3
"""
Canonical entity extraction for knowledge graphs.
Follows strict naming rules with confidence scoring and variant detection.
"""

import spacy
import json
import re
from collections import defaultdict
from pathlib import Path

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# Canonical term mappings: variations → canonical name
CANONICAL_TERMS = {
    # ANOVA variations
    'analysis of variance': 'ANOVA',
    'anova': 'ANOVA',
    'two-way anova': 'two-way ANOVA',
    'one-way anova': 'one-way ANOVA',
    'two-factor anova': 'two-factor ANOVA',

    # Design types
    'design of experiments': 'DOE',
    'doe': 'DOE',
    'experimental design': 'DOE',
    'full factorial design': 'full factorial design',
    'full factorial': 'full factorial design',
    'fractional factorial design': 'fractional factorial design',
    'fractional factorial': 'fractional factorial design',
    'half fraction': 'half-fraction design',
    'half-fraction': 'half-fraction design',
    'central composite design': 'central composite design',
    'ccd': 'central composite design',
    'box-behnken design': 'Box-Behnken design',
    'plackett-burman design': 'Plackett-Burman design',
    'plackett burman': 'Plackett-Burman design',
    'latin square': 'Latin square design',
    'latin square design': 'Latin square design',

    # Statistical tests
    "student's t-test": 't-test',
    't test': 't-test',
    't-test': 't-test',
    'f-test': 'F-test',
    'f test': 'F-test',

    # Effects and interactions
    'main effect': 'main effect',
    'main effects': 'main effect',
    'interaction': 'interaction',
    'interaction effect': 'interaction',
    'two-factor interaction': 'two-factor interaction',
    'two factor interaction': 'two-factor interaction',
    '2fi': 'two-factor interaction',
    'three-factor interaction': 'three-factor interaction',
    'three factor interaction': 'three-factor interaction',
    '3fi': 'three-factor interaction',

    # Model types
    'least squares': 'least squares',
    'least squares model': 'least squares model',
    'linear model': 'linear model',
    'quadratic model': 'quadratic model',
    'regression model': 'regression model',
    'regression': 'regression',

    # Design concepts
    'blocking': 'blocking',
    'confounding': 'confounding',
    'aliasing': 'aliasing',
    'alias': 'aliasing',
    'randomization': 'randomization',
    'replication': 'replication',
    'replicate': 'replication',

    # Parameters and statistics
    'variance': 'variance',
    'standard deviation': 'standard deviation',
    'standard error': 'standard error',
    'coefficient': 'coefficient',
    'intercept': 'intercept',
    'slope': 'slope',
    'residual': 'residual',
    'error': 'error',

    # Experimental elements
    'factor': 'factor',
    'level': 'level',
    'treatment': 'treatment',
    'response': 'response variable',
    'response variable': 'response variable',
    'run': 'experimental run',
    'experiment': 'experiment',
    'trial': 'trial',
    'observation': 'observation',

    # Design properties
    'resolution': 'design resolution',
    'generator': 'generator',
    'defining relationship': 'defining relationship',
    'contrast': 'contrast',
    'confounding pattern': 'confounding pattern',

    # Optimization
    'optimization': 'optimization',
    'response surface': 'response surface methodology',
    'rsm': 'response surface methodology',
    'steepest ascent': 'steepest ascent',
    'steepest descent': 'steepest descent',

    # Analysis methods
    'screening': 'screening design',
    'screening design': 'screening design',
    'curvature': 'curvature',
    'foldover': 'foldover design',
    'projectivity': 'projectivity',

    # Statistical concepts
    'significance': 'statistical significance',
    'p-value': 'p-value',
    'confidence interval': 'confidence interval',
    'hypothesis test': 'hypothesis test',
    'null hypothesis': 'null hypothesis',
    'alternative hypothesis': 'alternative hypothesis',
    'type i error': 'Type I error',
    'type ii error': 'Type II error',
    'alpha': 'alpha',
    'beta': 'beta',
    'power': 'statistical power',
    'statistical power': 'statistical power',

    # Other
    'bias': 'bias',
    'disturbance': 'disturbance',
    'ofat': 'OFAT',
    'cost': 'COST',
    'one-variable-at-a-time': 'OFAT',
    'change one single variable at a time': 'COST',
}

# Greek letter mappings
GREEK_LETTERS = {
    'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
    'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta',
    'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi',
    'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau',
    'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
}

# Abbreviation pairs (full form → abbreviation)
ABBREVIATIONS = {
    'analysis of variance': 'ANOVA',
    'design of experiments': 'DOE',
    'central composite design': 'CCD',
    'response surface methodology': 'RSM',
    'one-variable-at-a-time': 'OFAT',
    'change one single variable at a time': 'COST',
    'two-factor interaction': '2FI',
    'three-factor interaction': '3FI',
}

# Variants (canonical → variant)
VARIANTS = {
    'ANOVA': ['two-way ANOVA', 'one-way ANOVA', 'two-factor ANOVA'],
    'full factorial design': ['2^k factorial', '2^3 factorial', '2^4 factorial'],
    'fractional factorial design': ['half-fraction design', '2^(k-p) design'],
}

# Stopwords (expanded list)
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
    'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
}

def normalize_term(text):
    """Normalize a term for matching."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[.,;:!?]+$', '', text)
    return text

def remove_stopwords(text):
    """Remove leading/trailing stopwords from entity."""
    words = text.split()
    # Remove leading stopwords
    while words and words[0].lower() in STOPWORDS:
        words.pop(0)
    # Remove trailing stopwords
    while words and words[-1].lower() in STOPWORDS:
        words.pop()
    return ' '.join(words)

def get_canonical_name(text):
    """Get canonical name for a term."""
    normalized = normalize_term(text)
    return CANONICAL_TERMS.get(normalized, None)

def convert_greek_letters(text):
    """Convert Greek letters to words."""
    for greek, word in GREEK_LETTERS.items():
        text = text.replace(greek, word)
    return text

def calculate_confidence(text, sentence, doc):
    """Calculate confidence score for an entity extraction."""
    confidence = 0.5  # Base confidence

    normalized = normalize_term(text)

    # Higher confidence if it's a known canonical term
    if normalized in CANONICAL_TERMS:
        confidence += 0.3

    # Higher confidence if term appears multiple times in sentence
    term_count = sentence.lower().count(normalized)
    if term_count > 1:
        confidence += 0.1

    # Higher confidence if it's capitalized (likely important)
    if text[0].isupper() and len(text) > 1:
        confidence += 0.1

    # Lower confidence if very short
    if len(text) < 4:
        confidence -= 0.2

    # Cap at 1.0
    return min(1.0, max(0.0, confidence))

def extract_entities_canonical(text, current_file, start_line):
    """Extract entities using canonical naming rules."""
    entities = []
    doc = nlp(text)

    seen_in_section = set()

    # Extract noun chunks
    for chunk in doc.noun_chunks:
        chunk_text = convert_greek_letters(chunk.text)
        chunk_text = remove_stopwords(chunk_text)

        if not chunk_text or len(chunk_text) < 3:
            continue

        normalized = normalize_term(chunk_text)

        # Check if it maps to a canonical term
        canonical = get_canonical_name(chunk_text)

        if canonical:
            # Create unique key for deduplication
            unique_key = (canonical, chunk.sent.text[:100])

            if unique_key not in seen_in_section:
                line_offset = text[:chunk.start_char].count('\n')
                confidence = calculate_confidence(chunk_text, chunk.sent.text, doc)

                entities.append({
                    "entity": canonical,
                    "type": "concept",
                    "context": chunk.sent.text.strip()[:150],
                    "confidence": round(confidence, 2),
                    "file": current_file,
                    "line": start_line + line_offset
                })

                seen_in_section.add(unique_key)

    # Look for specific patterns with regex
    patterns = [
        (r'\b(two|three|four)-factor interaction\b', 'interaction'),
        (r'\b2\^k\b|\b2\^\{?k-?p?\}?\b', 'factorial design'),
        (r'\bp-value\b|p\s*<\s*0\.\d+', 'p-value'),
        (r'\balpha\s*=\s*0\.\d+', 'alpha'),
        (r'\bR\^2\b|\bR-squared\b', 'R-squared'),
    ]

    for pattern, entity_type in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            matched_text = match.group()
            canonical = get_canonical_name(matched_text)

            if canonical:
                # Find which sentence this is in
                match_pos = match.start()
                sent_text = ""
                for sent in doc.sents:
                    if sent.start_char <= match_pos <= sent.end_char:
                        sent_text = sent.text
                        break

                line_offset = text[:match_pos].count('\n')

                entities.append({
                    "entity": canonical,
                    "type": "concept",
                    "context": sent_text.strip()[:150],
                    "confidence": 0.8,
                    "file": current_file,
                    "line": start_line + line_offset
                })

    return entities

def process_text_file(input_file):
    """Process the extracted text file."""
    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by file markers
    file_sections = re.split(r'={80}\nFILE: (.+?)\n={80}\n', content)

    all_entities = []

    # Extract entities from each file section
    print("\nExtracting canonical entities...")
    for i in range(1, len(file_sections), 2):
        if i+1 >= len(file_sections):
            break

        current_file = file_sections[i].strip()
        text = file_sections[i+1]

        print(f"  Processing {current_file}...")
        entities = extract_entities_canonical(text, current_file, start_line=1)
        all_entities.extend(entities)

    return all_entities

def main():
    """Main extraction process."""
    input_file = Path('/home/user/pid-book/doe_extracted_text.txt')

    # Extract entities
    entities = process_text_file(input_file)

    # Save as JSON array
    output_file = Path('/home/user/pid-book/entities_canonical.json')

    print(f"\nSaving entities to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)

    # Statistics
    print("\n" + "="*80)
    print("CANONICAL EXTRACTION STATISTICS")
    print("="*80)
    print(f"Total entity extractions: {len(entities)}")

    # Count unique entities
    unique_entities = set(e['entity'] for e in entities)
    print(f"Unique canonical entities: {len(unique_entities)}")

    # Average confidence
    avg_confidence = sum(e['confidence'] for e in entities) / len(entities) if entities else 0
    print(f"Average confidence: {avg_confidence:.2f}")

    # Top entities
    from collections import Counter
    entity_counts = Counter(e['entity'] for e in entities)

    print("\n" + "="*80)
    print("TOP 30 CANONICAL ENTITIES")
    print("="*80)
    for entity, count in entity_counts.most_common(30):
        print(f"{entity:50s} ({count} occurrences)")

    print("\n" + "="*80)
    print("Extraction complete!")
    print("="*80)

if __name__ == '__main__':
    main()
