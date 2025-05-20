import hashlib

def check_position_140():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    # Expected text
    text = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Get words
    words = text.split()

    # Focus on position 140
    position = 140
    expected_word = words[position].strip(".,!?;:'\"").lower()
    actual_hash = hashes[position]

    print(f"Position {position}: Expected word is '{expected_word}'")
    print(f"Hash at position {position}: {actual_hash}")

    # Check exact match
    expected_word_bytes = expected_word.encode("utf-8")
    expected_hash = hashlib.md5(key_bytes + expected_word_bytes).hexdigest()

    print(f"Hash for '{expected_word}': {expected_hash}")
    print(f"Hash match: {'✓' if expected_hash == actual_hash else '✗'}")

    # Try with comma
    with_comma = expected_word + ","
    with_comma_bytes = with_comma.encode("utf-8")
    with_comma_hash = hashlib.md5(key_bytes + with_comma_bytes).hexdigest()

    print(f"Hash for '{with_comma}': {with_comma_hash}")
    print(f"Match with comma: {'✓' if with_comma_hash == actual_hash else '✗'}")

    # Check "to"
    to_bytes = "to".encode("utf-8")
    to_hash = hashlib.md5(key_bytes + to_bytes).hexdigest()

    print(f"Hash for 'to': {to_hash}")
    print(f"'to' matches: {'✓' if to_hash == actual_hash else '✗'}")

    # Check words surrounding position 140
    print("\nWords around position 140:")
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

    # Now let's check all variants of "tom" with and without punctuation
    print("\nChecking variants of 'tom':")
    variants = ["tom", "Tom", "tom,", "Tom,", "TOM", "TOM,"]

    for variant in variants:
        variant_bytes = variant.encode("utf-8")
        variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

        match = "✓" if variant_hash == actual_hash else "✗"
        print(f"'{variant}' -> {match}")

    # Now let's try dropping letters from words in the message to see if any match
    print("\nChecking all single-letter deletions from position 140 word:")
    for i in range(len(expected_word)):
        deleted = expected_word[:i] + expected_word[i+1:]
        deleted_bytes = deleted.encode("utf-8")
        deleted_hash = hashlib.md5(key_bytes + deleted_bytes).hexdigest()

        match = "✓" if deleted_hash == actual_hash else "✗"
        print(f"'{expected_word}' without '{expected_word[i]}' = '{deleted}' -> {match}")

        # Also try with comma
        deleted_comma = deleted + ","
        deleted_comma_bytes = deleted_comma.encode("utf-8")
        deleted_comma_hash = hashlib.md5(key_bytes + deleted_comma_bytes).hexdigest()

        match = "✓" if deleted_comma_hash == actual_hash else "✗"
        print(f"'{expected_word},' without '{expected_word[i]}' = '{deleted_comma}' -> {match}")

if __name__ == "__main__":
    check_position_140()