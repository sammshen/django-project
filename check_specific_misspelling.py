import hashlib

def check_specific_misspelling():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # Words to check for specific misspellings
    words_to_check = [
        "hashes", "those", "grass", "full", "bright", "i", "day", "night",
        "lightning", "canvas", "miss", "watsons", "door", "foot", "tomorrow",
        "sadies", "recipe", "slaves", "life", "more", "demands", "food", "days",
        "christian", "all", "boys", "huck", "tom"
    ]

    # Specific misspelling to check
    for word in words_to_check:
        misspelled = "hases" if word == "hashes" else None

        # Generate other potential misspellings
        misspellings = []
        if misspelled:
            misspellings.append(misspelled)

        # Common misspelling patterns (examples)
        misspellings.extend([
            # Omitting characters
            word[:-1] if len(word) > 1 else "",  # omit last character
            word[1:] if len(word) > 1 else "",   # omit first character

            # Swapping adjacent characters if word is long enough
            word[:1] + word[2:] if len(word) >= 3 else "",  # omit second character

            # Common character confusions
            word.replace('a', 'e') if 'a' in word else "",
            word.replace('e', 'a') if 'e' in word else "",

            # Double letter reduced to single
            word.replace('ss', 's') if 'ss' in word else "",
            word.replace('ee', 'e') if 'ee' in word else "",
            word.replace('tt', 't') if 'tt' in word else "",
            word.replace('ll', 'l') if 'll' in word else "",
            word.replace('mm', 'm') if 'mm' in word else "",
            word.replace('nn', 'n') if 'nn' in word else "",
        ])

        # Remove empty strings
        misspellings = [m for m in misspellings if m]

        # Check if any misspelling matches a hash
        for misspelled in misspellings:
            misspelled_bytes = misspelled.encode("utf-8")
            misspelled_hash = hashlib.md5(key_bytes + misspelled_bytes).hexdigest()

            if misspelled_hash in hash_set:
                print(f"Found misspelling: '{misspelled}' should be '{word}'")

    # Specifically check if "hases" is in the hashes
    misspelled = "hases"
    misspelled_bytes = misspelled.encode("utf-8")
    misspelled_hash = hashlib.md5(key_bytes + misspelled_bytes).hexdigest()

    if misspelled_hash in hash_set:
        print(f"Confirmed: 'hases' is in the puzzle hashes (misspelling of 'hashes')")
    else:
        print(f"'hases' is not in the puzzle hashes")

    # Additionally, check every possible word with "hases" substring
    print("\nChecking all words containing 'hases'...")
    word_found = False

    with open('/usr/share/dict/words', 'r') as dictionary:
        for word in dictionary:
            word = word.strip().lower()
            if "hases" in word:
                word_bytes = word.encode("utf-8")
                word_hash = hashlib.md5(key_bytes + word_bytes).hexdigest()

                if word_hash in hash_set:
                    print(f"Found word with 'hases': '{word}'")
                    word_found = True

    if not word_found:
        print("No words containing 'hases' found in the puzzle.")

if __name__ == "__main__":
    check_specific_misspelling()