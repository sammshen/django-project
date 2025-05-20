import hashlib

def find_misspelled_word():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # The expected message with each word in the correct order
    text = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Split into words and clean them
    words = text.split()
    clean_words = [word.strip(".,!?;:'\"").lower() for word in words]

    # Read the hashes in order
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Directly check each word against its corresponding hash
    print(f"Checking {len(clean_words)} words against {len(hashes)} hashes...")

    for i, (word, expected_hash) in enumerate(zip(clean_words, hashes)):
        # Calculate hash for this word
        word_bytes = word.encode("utf-8")
        actual_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        # Compare with expected hash
        if actual_hash != expected_hash:
            print(f"Mismatch at position {i}: Word '{word}' does not match hash")
            print(f"Expected hash: {expected_hash}")
            print(f"Actual hash:   {actual_hash}")

            # Find what word does match this hash
            for test_word in clean_words:
                test_bytes = test_word.encode("utf-8")
                test_hash = hashlib.md5(key_bytes + test_bytes).hexdigest()

                if test_hash == expected_hash:
                    print(f"Instead of '{word}', the hash matches '{test_word}'")

            # Try common typos
            print(f"\nTrying typos of '{word}':")

            # Missing letter variants
            for j in range(len(word)):
                variant = word[:j] + word[j+1:]
                variant_bytes = variant.encode("utf-8")
                variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

                if variant_hash == expected_hash:
                    print(f"- Missing letter: '{variant}' (missing '{word[j]}') matches the hash")

            # Additional letter variants
            for j in range(len(word)+1):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    variant = word[:j] + c + word[j:]
                    variant_bytes = variant.encode("utf-8")
                    variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

                    if variant_hash == expected_hash:
                        print(f"- Added letter: '{variant}' matches the hash")

            # Try all other words
            for test_word in set(clean_words) - {word}:
                test_bytes = test_word.encode("utf-8")
                test_hash = hashlib.md5(key_bytes + test_bytes).hexdigest()

                if test_hash == expected_hash:
                    print(f"- Word '{test_word}' matches the hash instead")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    find_misspelled_word()