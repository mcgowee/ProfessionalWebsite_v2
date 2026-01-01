from flask import jsonify
from collections import Counter

TOP_N_DEFAULT = 9

# Load the word list on module load
with open("words.txt", "r") as file:
    word_list = [
        line.strip().lower()
        for line in file
        if len(line.strip()) == 5 and line.strip().isalpha()
    ]

def normalize_guess(g: str) -> str:
    g = (g or "").strip().lower()
    return g

def normalize_feedback(f: str) -> str:
    f = (f or "").strip().lower()
    return f

def wordle_feedback(target: str, guess: str) -> str:
    """
    Return Wordle-accurate feedback string of length 5 using:
      g = green (correct letter, correct position)
      y = yellow (correct letter, wrong position, respecting counts)
      b = gray/blank (letter not present or overused)
    Duplicate letters are handled like real Wordle.
    """
    target = target.lower()
    guess = guess.lower()

    result = ["b"] * 5

    # First pass: greens
    remaining = []
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = "g"
        else:
            remaining.append(target[i])

    # Count remaining letters (non-green positions only)
    counts = Counter(remaining)

    # Second pass: yellows
    for i in range(5):
        if result[i] == "g":
            continue
        ch = guess[i]
        if counts.get(ch, 0) > 0:
            result[i] = "y"
            counts[ch] -= 1

    return "".join(result)

def calculate_letter_frequency(words):
    # Favor unique letters (good for exploration)
    freq = {}
    for word in words:
        for letter in set(word):
            freq[letter] = freq.get(letter, 0) + 1
    return freq

def score_words(words, freq):
    scores = []
    for word in words:
        unique_letters = set(word)
        score = sum(freq.get(letter, 0) for letter in unique_letters)
        scores.append((word, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)

def matches_feedback(candidate: str, guess: str, feedback: str) -> bool:
    # Compare the real Wordle feedback to the user-provided feedback
    return wordle_feedback(candidate, guess) == feedback

def filter_words(words, guesses, feedbacks):
    for guess, feedback in zip(guesses, feedbacks):
        words = [w for w in words if matches_feedback(w, guess, feedback)]
    return words

def process_wordle_request(data):
    history = data.get("history", [])
    top_n = int(data.get("top_n", TOP_N_DEFAULT))

    if not history or not all(isinstance(pair, list) and len(pair) == 2 for pair in history):
        return jsonify({"error": "Invalid input format. Expecting list of [guess, feedback] pairs."}), 400

    guesses = [normalize_guess(pair[0]) for pair in history]
    feedbacks = [normalize_feedback(pair[1]) for pair in history]

    # Validate inputs
    for g, f in zip(guesses, feedbacks):
        if len(g) != 5 or not g.isalpha():
            return jsonify({"error": "Each guess must be exactly 5 letters (a-z)."}), 400
        if len(f) != 5 or any(c not in "byg" for c in f):
            return jsonify({"error": "Each feedback must be 5 chars using only b/y/g."}), 400

    # Filter candidates using Wordle-accurate scoring
    filtered_words = filter_words(word_list, guesses, feedbacks)

    # Score remaining words
    freq = calculate_letter_frequency(filtered_words)
    scored_words = score_words(filtered_words, freq)

    top_suggestions = [{"word": w, "score": s} for w, s in scored_words[:top_n]]

    return jsonify({
        "remaining_count": len(filtered_words),
        "top_suggestions": top_suggestions
    })
