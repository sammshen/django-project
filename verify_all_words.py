import hashlib

def verify_all_words():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Full expected message
    expected_message = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Split by spaces for processing
    words = expected_message.split()
    # Clean for matching (lowercase, no punctuation)
    clean_words = [word.strip(".,!?;:'\"").lower() for word in words]

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Create dictionary to track incorrect hashes
    incorrect_hashes = []

    # For each hash, try all words to find the one it should match
    print(f"Checking each hash against its expected word in the message...")
    print(f"Words: {len(words)}, Hashes: {len(hashes)}")

    # For each word position in the message
    for i, (word, clean_word) in enumerate(zip(words, clean_words)):
        # Skip if we've run out of hashes
        if i >= len(hashes):
            break

        # Get the expected hash for this position
        expected_hash = hashes[i]

        # Calculate hash for the clean word
        word_bytes = clean_word.encode("utf-8")
        actual_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        # Compare expected and actual hash
        if actual_hash != expected_hash:
            incorrect_hashes.append((i, word, expected_hash))
            print(f"Position {i:3d}: '{word}' -> Expected hash does not match")

            # Try special cases (possessives, etc.)
            special_cases = [
                word.lower(),
                word.strip(".,!?;:'\"").lower(),
                word.strip(".,!?;:'\"").lower().replace("'s", "s"),
                word.strip(".,!?;:'\"").lower().replace("'", "")
            ]

            for special_case in special_cases:
                special_bytes = special_case.encode("utf-8")
                special_hash = hashlib.md5(key_bytes + special_bytes).hexdigest()

                if special_hash == expected_hash:
                    print(f"  - special case '{special_case}' matches")

    # Summarize findings
    print(f"\nFound {len(incorrect_hashes)} incorrectly hashed words")

    # Check if any hased matches particular words
    print("\nChecking for misspellings like 'hases' instead of 'hashes'...")
    possible_misspellings = ["hases", "hashs", "hashes", "hasches", "hashess"]

    for word in possible_misspellings:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hashes:
            position = hashes.index(word_hash)
            print(f"Found '{word}' at position {position}")

    # Check missing letter variations
    word = "hashes"
    for i in range(len(word)):
        variant = word[:i] + word[i+1:]
        variant_bytes = variant.encode("utf-8")
        variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

        if variant_hash in hashes:
            position = hashes.index(variant_hash)
            print(f"Found '{variant}' at position {position}")

if __name__ == "__main__":
    verify_all_words()