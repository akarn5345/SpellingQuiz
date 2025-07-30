import csv
import json
import random

def format_word(word):
    word = word.strip().lower()
    return word.capitalize()

def generate_options(correct_word, all_words):
    first_letter = correct_word[0].lower()
    correct_word = format_word(correct_word)
    wrong_options = []

    # Filter out words with same first letter but different from correct word
    candidates = [w for w in all_words if w.lower() != correct_word.lower() and w[0].lower() == first_letter]

    # Make sure to pick 3 unique incorrect options
    while len(wrong_options) < 3 and candidates:
        choice = format_word(random.choice(candidates))
        if choice not in wrong_options:
            wrong_options.append(choice)

    all_choices = wrong_options + [correct_word]
    random.shuffle(all_choices)

    correct_letter = chr(ord('A') + all_choices.index(correct_word))
    options_dict = {chr(ord('A') + i): word for i, word in enumerate(all_choices)}

    return options_dict, correct_letter

def generate_quiz_data(input_csv, output_json):
    all_words = []
    questions = []

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_words.append(row['Word'])

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            correct_word = row['Word']
            year = row.get('Year', '2024')
            options, correct_letter = generate_options(correct_word, all_words)
            question = {
                "correct_word": format_word(correct_word),
                "options": options,
                "correct_letter": correct_letter,
                "year": year
            }
            questions.append(question)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

# Run this function with actual file paths
generate_quiz_data("word_list.csv", "quiz_data.json")
