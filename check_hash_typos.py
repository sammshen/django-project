import hashlib

def check_hash_typos():
    key = "485066843"
    key_bytes = key.encode("utf-8")

    # Read the puzzle hashes
    with open("puzzle/PUZZLE", "r") as f:
        hashes = [line.strip() for line in f.readlines()]

    hash_set = set(hashes)

    # List of words to check for typos
    words_to_check = [
        "hash", "hashes", "hashing", "hasher", "hashy",
        "has", "hase", "hases", "hasch", "hashe",
        "hsh", "hsah", "hsaes", "hsahes", "ahses", "ashesh"
    ]

    # Generate potential typos for "hashes"
    word = "hashes"
    typos = []

    # Missing letters
    for i in range(len(word)):
        typos.append(word[:i] + word[i+1:])

    # Extra letters
    for i in range(len(word) + 1):
        for c in "abcdefghijklmnopqrstuvwxyz":
            typos.append(word[:i] + c + word[i:])

    # Swapped letters
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        typos.append(''.join(swapped))

    # Wrong letters
    for i in range(len(word)):
        for c in "abcdefghijklmnopqrstuvwxyz":
            if c != word[i]:
                typos.append(word[:i] + c + word[i+1:])

    # Add from words_to_check
    typos.extend(words_to_check)

    # Remove duplicates
    typos = list(set(typos))

    print(f"Checking {len(typos)} possible variations...")

    # Check if any of these typos appear in the puzzle
    for typo in typos:
        typo_bytes = typo.encode("utf-8")
        typo_hash = hashlib.md5(key_bytes + typo_bytes).hexdigest()

        if typo_hash in hash_set:
            print(f"Found! Typo '{typo}' appears in the puzzle (could be a misspelling of 'hashes')")

if __name__ == "__main__":
    check_hash_typos()