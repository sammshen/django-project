import hashlib

def find_incorrect_hash():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # The expected message split into words
    expected_message = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Split by spaces, keeping punctuation
    words = expected_message.split()

    # Clean each word for hashing (remove punctuation at the beginning/end only)
    clean_words = []
    for word in words:
        # Remove punctuation from beginning and end
        clean_word = word.strip(".,!?;:'\"")
        clean_words.append((clean_word, word))  # (clean word for hashing, original word)

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Verify the word count matches
    print(f"Words in message: {len(clean_words)}")
    print(f"Hashes in puzzle: {len(hashes)}")

    if len(clean_words) != len(hashes):
        print("WARNING: Word count doesn't match hash count!")

    # Check each word against its corresponding hash
    matched_words = []
    unmatched_words = []

    for i, (clean_word, original_word) in enumerate(clean_words):
        # Skip if we've run out of hashes
        if i >= len(hashes):
            break

        # Get the hash at the same position
        expected_hash = hashes[i]

        # Calculate the hash for this word
        word_bytes = clean_word.lower().encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        # Check if it matches
        if word_hash == expected_hash:
            matched_words.append((i, original_word))
        else:
            unmatched_words.append((i, original_word, expected_hash))
            print(f"Mismatch at position {i}: '{original_word}' does not match hash {expected_hash}")

            # Try common variations
            variations = [
                clean_word.lower(),               # lowercase
                clean_word.upper(),               # uppercase
                clean_word.lower().replace("'s", "s"),  # remove apostrophe in possessives
                clean_word.lower().replace("'", "")     # remove all apostrophes
            ]

            # Check if any variation matches
            matched = False
            for var in variations:
                var_bytes = var.encode("utf-8")
                var_hash = hashlib.md5(key_bytes + var_bytes).hexdigest()

                if var_hash == expected_hash:
                    print(f"  - Variation '{var}' matches the hash")
                    matched = True

            if not matched:
                print(f"  - No common variation matches the hash")

    # Print summary
    print(f"\nResults: {len(matched_words)}/{len(clean_words)} words matched their expected hashes")

    # Try to find the correct word for each unmatched hash
    print("\nAttempting to correct unmatched words...")

    # Create a set of all words for quick lookup
    all_words = set(word.lower().strip(".,!?;:'\"") for word, _ in clean_words)

    for i, original_word, expected_hash in unmatched_words:
        # Try variations of the word
        variations = generate_variations(original_word.lower().strip(".,!?;:'\""))

        found = False
        for var in variations:
            var_bytes = var.encode("utf-8")
            var_hash = hashlib.md5(key_bytes + var_bytes).hexdigest()

            if var_hash == expected_hash:
                print(f"Position {i}: '{original_word}' should be '{var}'")
                found = True
                break

        if not found:
            # Try all words in our vocabulary
            for word in all_words:
                word_bytes = word.encode("utf-8")
                word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                if word_hash == expected_hash:
                    print(f"Position {i}: '{original_word}' should be '{word}'")
                    found = True
                    break

        if not found:
            print(f"Position {i}: Could not find a match for '{original_word}'")

def generate_variations(word):
    """Generate variations of a word to test for misspellings."""
    variations = []

    # Original word
    variations.append(word)

    # Common endings
    if word.endswith('s'):
        variations.append(word[:-1])  # Remove trailing 's'
    else:
        variations.append(word + 's')  # Add trailing 's'

    # Missing letters
    for i in range(len(word)):
        variations.append(word[:i] + word[i+1:])

    # Extra repeated letters
    for i in range(len(word)):
        variations.append(word[:i] + word[i] + word[i:])

    # Swapped adjacent letters
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variations.append(''.join(swapped))

    return variations

if __name__ == "__main__":
    find_incorrect_hash()