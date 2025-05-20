import hashlib

# The known 9-digit key
key = "485066843"
key_bytes = key.encode("utf-8")

# Read the puzzle hashes
with open("puzzle/PUZZLE", "r") as f:
    original_hashes = [line.strip() for line in f.readlines()]

# The known solution text from hw6-puzzlesolution.txt
solution_text = """Those little bastards were hiding out there in the tall grass. The moon was not quite full, but bright, and it was behind them, so I could see them as plain as day, though it was deep night. Lightning bugs flashed against the black canvas. I waited at Miss Watson's kitchen door, rocked a loose step board with my foot, knew she was going to tell me to fix it tomorrow. I was waiting there for her to give me a pan of corn bread that she had made with my Sadie's recipe. Waiting is a big part of a slave's life, waiting and waiting to wait some more. Waiting for demands. Waiting for food. Waiting for the ends of days. Waiting for the just and deserved Christian reward at the end of it all. Those white boys, Huck and Tom, watched me."""

# Split the solution into words
solution_words = solution_text.split()

# Verify the word count matches the hash count
if len(solution_words) != len(original_hashes):
    print(f"Warning: Word count mismatch! Solution has {len(solution_words)} words, but puzzle has {len(original_hashes)} hashes.")

# Check each word
mismatches = []
for i, word in enumerate(solution_words):
    if i < len(original_hashes):
        # Hash the word with the key
        word_hash = hashlib.md5(key_bytes + word.encode("utf-8")).hexdigest()

        # Compare with the original hash
        if word_hash != original_hashes[i]:
            mismatches.append((i, word, word_hash, original_hashes[i]))

# Print results
print(f"Found {len(mismatches)} mismatches:")
for i, word, calculated_hash, original_hash in mismatches:
    print(f"Index {i}: Word '{word}' generates hash {calculated_hash}")
    print(f"              but original hash is {original_hash}")
    print("-" * 70)

# Try alternative spellings for the mismatched words
print("\nTrying alternative spellings for mismatched words:")
for i, word, _, original_hash in mismatches:
    # Try some common misspellings or variations
    misspellings = []

    # Remove apostrophe
    if "'" in word:
        misspellings.append(word.replace("'", ""))

    # Swap letters
    for j in range(len(word)-1):
        swapped = list(word)
        swapped[j], swapped[j+1] = swapped[j+1], swapped[j]
        misspellings.append(''.join(swapped))

    # Add/remove single letters
    for j in range(len(word)+1):
        # Skip apostrophes
        if j > 0 and j < len(word) and word[j-1] == "'":
            continue

        # Remove a letter
        if j < len(word):
            removed = word[:j] + word[j+1:]
            misspellings.append(removed)

        # Add each letter of the alphabet
        for char in "abcdefghijklmnopqrstuvwxyz":
            added = word[:j] + char + word[j:]
            misspellings.append(added)

    # Change capitalization
    misspellings.append(word.capitalize())
    misspellings.append(word.lower())
    misspellings.append(word.upper())

    # Try each misspelling
    for misspelled in misspellings:
        misspelled_hash = hashlib.md5(key_bytes + misspelled.encode("utf-8")).hexdigest()
        if misspelled_hash == original_hash:
            print(f"Found match for index {i}!")
            print(f"Original word: '{word}'")
            print(f"Correct spelling: '{misspelled}'")
            print("-" * 70)