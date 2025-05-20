import hashlib

def check_hases():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # Words to check
    words_to_check = [
        "hash", "hashes", "hashs", "hase", "hases", "hashs",
        "hashe", "hashem", "hashey", "hashesh", "hashets",
        # Variations of "has"
        "has", "hase", "hass", "hasse", "hasy", "hasy's",
        # Variations without 'h'
        "ashes", "ashe", "ases", "asey", "ashy",
        # Variations with dropped letters
        "hases", "hahes", "hshes", "haes", "hahs", "hases", "hashs"
    ]

    print("Checking for matches with 'hases' and similar words...")

    for word in words_to_check:
        word_bytes = word.encode("utf-8")
        word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

        if word_hash in hash_set:
            # Find the position of this hash
            hash_position = hashes.index(word_hash)
            print(f"FOUND! Word '{word}' is in the puzzle at position {hash_position}")

            # Check if it's a common word but with a typo
            if word in ["hases", "hashs"]:
                print(f"This appears to be a misspelling of 'hashes'")

    print("\nChecking every single variation of 'hashes'...")

    # Generate all possible variants of "hashes" by changing one letter at a time
    word = "hashes"
    for i in range(len(word)):
        # Deletion
        deletion = word[:i] + word[i+1:]

        # Check deletion
        deletion_bytes = deletion.encode("utf-8")
        deletion_hash = hashlib.md5(key_bytes + deletion_bytes).hexdigest()

        if deletion_hash in hash_set:
            hash_position = hashes.index(deletion_hash)
            print(f"FOUND! Deletion variant '{deletion}' is in puzzle at position {hash_position}")
            if deletion == "hases":
                print(f"Confirmed: 'hases' is a misspelling of 'hashes' (missing 'h')")

        # Substitution
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != word[i]:
                substitution = word[:i] + c + word[i+1:]

                # Check substitution
                subst_bytes = substitution.encode("utf-8")
                subst_hash = hashlib.md5(key_bytes + subst_bytes).hexdigest()

                if subst_hash in hash_set:
                    hash_position = hashes.index(subst_hash)
                    print(f"FOUND! Substitution variant '{substitution}' is in puzzle at position {hash_position}")

if __name__ == "__main__":
    check_hases()