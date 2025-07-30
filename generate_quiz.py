import csv
import json
import random
from collections import defaultdict

# Format the word
def format_word(word):
    return word.strip().capitalize()

# Generate wrong options
def generate_options(correct_word, all_words):
    first_letter = correct_word[0].lower()
    same_letter_words = [w for w in all_words if w.lower().startswith(first_letter) and w.lower() != correct_word.lower()]
    random.shuffle(same_letter_words)
    wrong_options = []

    for w in same_letter_words:
        if format_word(w) not in wrong_options and len(wrong_options) < 3:
            wrong_options.append(format_word(w))

    if len(wrong_options) < 3:
        fallback = [w for w in all_words if w.lower() != correct_word.lower() and format_word(w) not in wrong_options]
        random.shuffle(fallback)
        for w in fallback:
            if len(wrong_options) >= 3:
                break
            wrong_options.append(format_word(w))

    options = wrong_options + [format_word(correct_word)]
    random.shuffle(options)

    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == format_word(correct_word)][0]

    return labeled_options, correct_letter

# Generate the quiz
input_csv = 'word_list.csv'
output_json = 'quiz_data.json'

quiz_data = []

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    all_words = [row['Word'] for row in reader if 'Word' in row and row['Word'].strip()]

    for row in reader:
        if 'Word' not in row or not row['Word'].strip():
            continue

        correct_word = row['Word'].strip()
        year = row.get('Year') or '2024'

        options, correct_letter = generate_options(correct_word, all_words)

        quiz_data.append({
            'correct_word': format_word(correct_word),
            'year': year,
            'options': options,
            'correct_letter': correct_letter
        })

with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)

print(f"Quiz data written to {output_json} with {len(quiz_data)} questions.")
