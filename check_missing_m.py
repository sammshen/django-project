import hashlib

def check_missing_m():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Let's check if "to" matches anywhere in the puzzle
    to_bytes = "to".encode("utf-8")
    to_hash = hashlib.md5(key_bytes + to_bytes).hexdigest()

    to_positions = []
    for i, hash_value in enumerate(hashes):
        if hash_value == to_hash:
            to_positions.append(i)

    print(f"The word 'to' appears at positions: {to_positions}")

    # Let's check if "tom" would match anywhere
    tom_bytes = "tom".encode("utf-8")
    tom_hash = hashlib.md5(key_bytes + tom_bytes).hexdigest()

    tom_positions = []
    for i, hash_value in enumerate(hashes):
        if hash_value == tom_hash:
            tom_positions.append(i)

    print(f"The word 'tom' appears at positions: {tom_positions}")

    # Check position 140 which should be "Tom," in the original text
    pos_140_hash = hashes[140]

    # Try various forms of Tom
    test_words = ["Tom", "tom", "To", "to", "TOM", "toms", "Tom,"]

    for word in test_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        match = "✓" if word_hash == pos_140_hash else "✗"
        print(f"Position 140: '{word}' -> {match}")

    # Try removing the 'm' from each word that contains 'm' in the message
    print("\nChecking all words with missing 'm':")

    original_text = "Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."

    words = original_text.split()
    for i, word in enumerate(words):
        clean_word = word.strip(".,!?;:'\"").lower()
        if 'm' in clean_word:
            # Create variant without 'm'
            variant = clean_word.replace('m', '')
            variant_bytes = variant.encode("utf-8")
            variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

            if variant_hash in hashes:
                variant_pos = hashes.index(variant_hash)
                print(f"Word '{clean_word}' without 'm' becomes '{variant}' at position {variant_pos}")

    # Now check specifically for position 64
    pos_64_hash = hashes[64]
    pos_64_expected_word = "tell"  # Based on the original text

    # Check if "tell" matches
    tell_bytes = "tell".encode("utf-8")
    tell_hash = hashlib.md5(key_bytes + tell_bytes).hexdigest()

    print(f"\nPosition 64 hash: {pos_64_hash}")
    print(f"'tell' hash: {tell_hash}")
    print(f"Expected word 'tell' at position 64: {'✓' if tell_hash == pos_64_hash else '✗'}")

    # Check if "to" matches at position 64
    to_bytes = "to".encode("utf-8")
    to_hash = hashlib.md5(key_bytes + to_bytes).hexdigest()

    print(f"'to' hash: {to_hash}")
    print(f"Word 'to' at position 64: {'✓' if to_hash == pos_64_hash else '✗'}")

if __name__ == "__main__":
    check_missing_m()