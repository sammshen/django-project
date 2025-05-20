import hashlib

def find_misspellings():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # The expected message split into words
    expected_message = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    expected_words = expected_message.replace(".", "").replace(",", "").replace("'s", "s").lower().split()

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    print(f"Expected words: {len(expected_words)}")
    print(f"Hashed words: {len(hashes)}")

    # Try to encode each expected word and check if its hash appears
    found_words = []
    missing_words = []

    for word in expected_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hashes:
            found_words.append(word)
        else:
            missing_words.append(word)

    print(f"Found words: {len(found_words)}")
    print(f"Missing words: {len(missing_words)}")

    if missing_words:
        print("\nWords that don't match any hash (potential misspellings):")
        for word in missing_words:
            print(f"- '{word}'")

    # Let's also check for hashes that don't match any expected word
    # This will help us find misspelled words in the hashes
    unmatched_hashes = []
    for hash_value in hashes:
        matched = False
        for word in expected_words:
            word_bytes = word.encode("utf-8")
            word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

            if word_hash == hash_value:
                matched = True
                break

        if not matched:
            unmatched_hashes.append(hash_value)

    print(f"\nHashes that don't match any expected word: {len(unmatched_hashes)}")
    if unmatched_hashes:
        print("\nThese could contain misspelled words. Let's try similar variations...")

        # Check for common misspellings or variations
        for hash_value in unmatched_hashes:
            # Try common misspellings for each word
            for word in expected_words:
                # Generate common misspellings
                variations = generate_variations(word)

                for variation in variations:
                    var_bytes = variation.encode("utf-8")
                    var_hash = hashlib.md5(key_bytes + var_bytes).hexdigest()

                    if var_hash == hash_value:
                        print(f"Found misspelling: '{variation}' instead of '{word}'")
                        print(f"Hash: {hash_value}")

def generate_variations(word):
    """Generate common misspelling variations of a word."""
    variations = []

    # Simple single-character omissions
    for i in range(len(word)):
        variations.append(word[:i] + word[i+1:])

    # Simple single-character duplications
    for i in range(len(word)):
        variations.append(word[:i] + word[i] + word[i:])

    # Simple single-character transpositions
    for i in range(len(word)-1):
        variations.append(word[:i] + word[i+1] + word[i] + word[i+2:])

    # Common substitutions
    if 'a' in word:
        variations.append(word.replace('a', 'e', 1))
    if 'e' in word:
        variations.append(word.replace('e', 'a', 1))
    if 'i' in word:
        variations.append(word.replace('i', 'y', 1))
    if 'y' in word:
        variations.append(word.replace('y', 'i', 1))

    return variations

if __name__ == "__main__":
    find_misspellings()