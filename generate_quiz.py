import csv
import random
import json

def generate_fishy_option(word):
    if len(word) < 3:
        return word + random.choice('aeiou')

    variations = set()
    vowels = 'aeiou'

    # Replace vowels
    for i, char in enumerate(word):
        if char.lower() in vowels:
            for v in vowels:
                if v != char.lower():
                    variations.add(word[:i] + v + word[i+1:])

    # Duplicate characters
    for i in range(len(word)):
        variations.add(word[:i] + word[i] * 2 + word[i+1:])

    # Remove characters
    if len(word) > 4:
        for i in range(len(word)):
            variations.add(word[:i] + word[i+1:])

    # Swap adjacent letters
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        variations.add(''.join(swapped))

    variations.discard(word)
    return random.choice(list(variations)) if variations else word + random.choice('xyz')

# Read from CSV and store (word, year) tuples
words = []
with open('word_list.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header if present, comment out if not
    for row in reader:
        if len(row) >= 2:
            word = row[0].strip()
            try:
                year = int(row[1].strip())
            except ValueError:
                continue
            if word:
                words.append((word, year))

quiz = []

for word, year in words:
    incorrect = set()
    while len(incorrect) < 3:
        wrong = generate_fishy_option(word)
        if wrong != word:
            incorrect.add(wrong)

    options = [word] + list(incorrect)
    random.shuffle(options)

    option_keys = ['a', 'b', 'c', 'd']
    options_dict = dict(zip(option_keys, options))
    correct_letter = [k for k, v in options_dict.items() if v == word][0]

    quiz.append({
        "question": "Choose the correctly spelled word:",
        "options": options_dict,
        "correct_letter": correct_letter,
        "correct_word": word,
        "year": year
    })

with open('quiz_data.json', 'w') as f:
    json.dump(quiz, f, indent=2)

print("✅ quiz_data.json generated successfully.")
