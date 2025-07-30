import csv
import json
import random
from collections import Counter

# Format the word (capitalize only first letter)
def format_word(word):
    return word.strip().capitalize()

# Generate typo variants
def generate_typo_variants(word):
    word = word.lower()
    variants = set()
    vowels = 'aeiou'

    # Swap adjacent
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    # Omit one letter
    for i in range(len(word)):
        variants.add(word[:i] + word[i+1:])

    # Duplicate a letter
    for i in range(len(word)):
        variants.add(word[:i] + word[i] + word[i:])

    # Replace a vowel
    for i in range(len(word)):
        if word[i] in vowels:
            for v in vowels:
                if v != word[i]:
                    variants.add(word[:i] + v + word[i+1:])

    # Clean and return
    variants.discard(word)
    variants = [format_word(v) for v in variants if len(v) > 2 and v.lower() != word.lower()]
    random.shuffle(variants)
    return variants[:3]

# Generate options
def generate_options(correct_word, all_words):
    typo_options = generate_typo_variants(correct_word)

    if len(typo_options) < 3:
        fallback = [format_word(w) for w in all_words if w.lower() != correct_word.lower()]
        random.shuffle(fallback)
        for w in fallback:
            if format_word(w) not in typo_options and len(typo_options) < 3:
                typo_options.append(format_word(w))

    options = typo_options + [format_word(correct_word)]
    random.shuffle(options)

    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == format_word(correct_word)][0]

    return labeled_options, correct_letter

# Input/Output files
input_csv = 'word_list.csv'
output_json = 'quiz_data.json'

quiz_data = []
year_counter = Counter()

# Read once
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    rows = list(csv.DictReader(csvfile))
    all_words = [row['Word'] for row in rows if 'Word' in row and row['Word'].strip()]

    for row in rows:
        if 'Word' not in row or not row['Word'].strip():
            continue

        correct_word = row['Word'].strip()
        year = row.get('Year', '').strip()
        if not year:
            year = '2024'  # fallback default

        year_counter[year] += 1

        options, correct_letter = generate_options(correct_word, all_words)

        quiz_data.append({
            'correct_word': format_word(correct_word),
            'year': year,
            'options': options,
            'correct_letter': correct_letter
        })

# Write to JSON
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)

# Summary
print(f"✅ Quiz data written to '{output_json}' with {len(quiz_data)} questions.")
print("\n📊 Question count by year:")
for yr, count in sorted(year_counter.items()):
    print(f"  {yr}: {count} questions")
