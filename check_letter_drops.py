import hashlib

def check_letter_drops():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # The expected message split into words
    expected_message = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

    # Clean up and get unique words
    expected_words = expected_message.replace(".", "").replace(",", "").replace("'s", "s").lower().split()
    expected_words = list(set(expected_words))  # Get unique words

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # For each word, try dropping each letter and check if it matches a hash
    print("Checking for missing letter variants...")

    for word in expected_words:
        # Skip very short words
        if len(word) <= 2:
            continue

        # Try dropping each letter
        for i in range(len(word)):
            variant = word[:i] + word[i+1:]
            variant_bytes = variant.encode("utf-8")
            variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

            if variant_hash in hash_set:
                print(f"Found hash match for '{variant}' (original: '{word}', dropped: '{word[i]}')")

                # Check other common distortions
                print(f"  - Could be a misspelling of '{word}' with missing '{word[i]}' at position {i}")

        # Also check for doubled letters
        for i in range(len(word)-1):
            if word[i] == word[i+1]:  # If we have a doubled letter
                variant = word[:i] + word[i+1:]  # Remove one of the doubled letters
                variant_bytes = variant.encode("utf-8")
                variant_hash = hashlib.md5(key_bytes + variant_bytes).hexdigest()

                if variant_hash in hash_set:
                    print(f"Found hash match for '{variant}' (original: '{word}', reduced doubled letter: '{word[i]}{word[i+1]}')")

if __name__ == "__main__":
    check_letter_drops()