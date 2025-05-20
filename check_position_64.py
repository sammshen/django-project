import hashlib

def check_position_64():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Expected text
    text = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Get words
    words = text.split()

    # Focus on position 64
    position = 64
    expected_word = words[position].strip(".,!?;:'\"").lower()
    actual_hash = hashes[position]

    print(f"Position {position}: Expected word is '{expected_word}'")
    print(f"Hash at position {position}: {actual_hash}")

    # Check exact match
    expected_word_bytes = expected_word.encode("utf-8")
    expected_hash = hashlib.md5(key_bytes + expected_word_bytes).hexdigest()

    print(f"Hash for '{expected_word}': {expected_hash}")
    print(f"Hash match: {'✓' if expected_hash == actual_hash else '✗'}")

    # Check "to"
    to_bytes = "to".encode("utf-8")
    to_hash = hashlib.md5(key_bytes + to_bytes).hexdigest()

    print(f"Hash for 'to': {to_hash}")
    print(f"'to' matches: {'✓' if to_hash == actual_hash else '✗'}")

    # Check "tell"
    tell_bytes = "tell".encode("utf-8")
    tell_hash = hashlib.md5(key_bytes + tell_bytes).hexdigest()

    print(f"Hash for 'tell': {tell_hash}")
    print(f"'tell' matches: {'✓' if tell_hash == actual_hash else '✗'}")

    # Check words surrounding position 64
    print("\nWords around position 64:")
    start = max(0, position - 5)
    end = min(len(words), position + 5)

    for i in range(start, end):
        word = words[i].strip(".,!?;:'\"").lower()
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        match = "✓" if i == position and word_hash == actual_hash else "✗"
        print(f"Position {i}: '{word}' -> {match}")

    print("\nAnalyzing the original message context:")
    print(" ".join(words[max(0, position-10):min(len(words), position+10)]))

    # Now let's check if any word from the message matches the hash at position 64
    print("\nChecking all words in the message to find a match for position 64:")

    for word in set(w.strip(".,!?;:'\"").lower() for w in words):
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash == actual_hash:
            print(f"Found match: '{word}' generates the hash at position 64")

if __name__ == "__main__":
    check_position_64()