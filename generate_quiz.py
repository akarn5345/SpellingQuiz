import csv
import json
import random

# Format the word (only first letter capital)
def format_word(word):
    return word.strip().capitalize()

# Generate typo-based wrong options
def generate_typo_variants(word):
    word = word.lower()
    variants = set()
    vowels = 'aeiou'

    # 1. Swap adjacent letters
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    # 2. Omit one letter
    for i in range(len(word)):
        variants.add(word[:i] + word[i+1:])

    # 3. Duplicate a letter
    for i in range(len(word)):
        variants.add(word[:i] + word[i] + word[i:])

    # 4. Replace a vowel with another vowel
    for i in range(len(word)):
        if word[i] in vowels:
            for v in vowels:
                if v != word[i]:
                    variants.add(word[:i] + v + word[i+1:])

    # Remove exact match and short or duplicate entries
    variants.discard(word)
    variants = [format_word(v) for v in variants if len(v) > 2 and v.lower() != word.lower()]
    random.shuffle(variants)
    return variants[:3]  # Return top 3 typo-like options

# Generate final multiple choice options
def generate_options(correct_word, all_words):
    typo_options = generate_typo_variants(correct_word)

    # If less than 3 typo variants, fill with random words (fallback)
    if len(typo_options) < 3:
        fallback = [format_word(w) for w in all_words if w.lower() != correct_word.lower()]
        random.shuffle(fallback)
        for w in fallback:
            if format_word(w) not in typo_options and len(typo_options) < 3:
                typo_options.append(format_word(w))

    # Add correct word and shuffle
    options = typo_options + [format_word(correct_word)]
    random.shuffle(options)

    # Label A–D and determine correct answer
    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == format_word(correct_word)][0]

    return labeled_options, correct_letter

# Input and output file paths
input_csv = 'word_list.csv'
output_json = 'quiz_data.json'

quiz_data = []

# Read CSV and build quiz
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    rows = list(csv.DictReader(csvfile))
    all_words = [row['Word'] for row in rows if 'Word' in row and row['Word'].strip()]

    for row in rows:
        if 'Word' not in row or not row['Word'].strip():
            continue

        correct_word = row['Word'].strip()
        year = row.get('Year', '').strip() or '2024'

        options, correct_letter = generate_options(correct_word, all_words)

        quiz_data.append({
            'correct_word': format_word(correct_word),
            'year': year,
            'options': options,
            'correct_letter': correct_letter
        })

# Write to JSON file
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)

print(f"✅ Quiz data written to '{output_json}' with {len(quiz_data)} questions.")
