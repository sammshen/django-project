import hashlib

def final_check():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # From the original message
    original_text = "Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."

    # Check each position in the hash list
    for i, hash_value in enumerate(hashes):
        # 1. Try "hases" and related terms
        test_words = ["hases", "hashs", "hshes", "hahs", "hases", "hathes", "halses", "haskes", "hasees", "hashes"]

        for test_word in test_words:
            test_bytes = test_word.encode("utf-8")
            test_hash = hashlib.md5(key_bytes + test_bytes).hexdigest()

            if test_hash == hash_value:
                print(f"Position {i}: Found matching word '{test_word}' for hash {hash_value}")

    # Check if "hases" is a word in the original text
    print("\nChecking if 'hases' appears in the original text:")
    for word in original_text.split():
        clean_word = word.strip(".,!?;:'\"").lower()
        if clean_word in ["hases", "hashs", "hathes"]:
            print(f"Found '{clean_word}' in the original text")

    # Check if "hashes" appears in the original text
    print("\nChecking if 'hashes' appears in the original text:")
    for word in original_text.split():
        clean_word = word.strip(".,!?;:'\"").lower()
        if clean_word == "hashes":
            print(f"Found '{clean_word}' in the original text")

    # Calculate and print hash for both "hases" and "hashes"
    print("\nChecking hash values for 'hases' and 'hashes':")
    test_words = ["hases", "hashes"]
    for word in test_words:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()
        print(f"{word}: {word_hash}")
        if word_hash in hash_set:
            pos = hashes.index(word_hash)
            print(f"  - Found at position {pos}")

if __name__ == "__main__":
    final_check()