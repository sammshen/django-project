import hashlib
import string

# The known 9-digit key
key = "485066843"
key_bytes = key.encode("utf-8")

# Get the puzzle hashes
with open("puzzle/PUZZLE", "r") as f:
    original_hashes = [line.strip() for line in f]

# Words that didn't match from our first analysis
mismatches = [
    (49, "Watson's", "14b625c3727b384cb012e42a6e94df9d"),
    (73, "waiting", "9291c4d7338648be9c05d86fdb4124f9"),
    (91, "Sadie's", "8b17faffc9b2bc6ea78d05394c612c74"),
    (100, "slave's", "e8f042230c2e9f25cd9c030fe4645e13")
]

def hash_word(word):
    return hashlib.md5(key_bytes + word.encode("utf-8")).hexdigest()

# Function to try all possible single-character substitutions
def try_char_substitutions(word, target_hash):
    for i in range(len(word)):
        for char in string.ascii_letters + string.punctuation + string.digits:
            # Skip if it's the same character
            if word[i] == char:
                continue

            new_word = word[:i] + char + word[i+1:]
            hash_value = hash_word(new_word)

            if hash_value == target_hash:
                return new_word
    return None

# Try all possible combinations of uppercase/lowercase for the word
def try_case_variations(word, target_hash):
    import itertools

    # Generate all possible case variations
    chars = []
    for c in word:
        if c.isalpha():
            chars.append([c.lower(), c.upper()])
        else:
            chars.append([c])

    # Try each case variation
    for combo in itertools.product(*chars):
        variation = ''.join(combo)
        hash_value = hash_word(variation)

        if hash_value == target_hash:
            return variation

    return None

# Try all possible single-character insertions
def try_char_insertions(word, target_hash):
    for i in range(len(word) + 1):
        for char in string.ascii_letters + string.punctuation + string.digits:
            new_word = word[:i] + char + word[i:]
            hash_value = hash_word(new_word)

            if hash_value == target_hash:
                return new_word
    return None

# Try all possible single-character deletions
def try_char_deletions(word, target_hash):
    for i in range(len(word)):
        new_word = word[:i] + word[i+1:]
        hash_value = hash_word(new_word)

        if hash_value == target_hash:
            return new_word
    return None

# Try all possible adjacent character swaps
def try_char_swaps(word, target_hash):
    for i in range(len(word) - 1):
        new_word = word[:i] + word[i+1] + word[i] + word[i+2:]
        hash_value = hash_word(new_word)

        if hash_value == target_hash:
            return new_word
    return None

# Try removing apostrophes and possessives
def try_apostrophe_variations(word, target_hash):
    variations = []

    # Remove apostrophe
    if "'" in word:
        variations.append(word.replace("'", ""))

    # Remove apostrophe and s
    if "'s" in word:
        variations.append(word.replace("'s", ""))
        variations.append(word.replace("'s", "s"))

    # Add apostrophe or 's if not present
    if "'" not in word:
        for i in range(len(word)):
            variations.append(word[:i] + "'" + word[i:])
            variations.append(word[:i] + "'s" + word[i:])

    for variation in variations:
        hash_value = hash_word(variation)
        if hash_value == target_hash:
            return variation

    return None

# Try common misspellings for "Sadie's"
def try_sadie_variations(target_hash):
    variations = [
        "Sadie",
        "Sadies",
        "Sadier",
        "Saides",
        "Sadies'",
        "Saddies",
        "Sadys",
        "Sadys'",
        "Sady's",
        "Saddie's",
        "Sadye's",
        "Sadiey's",
        "Saidee's",
        "Saydee's",
        "Saydies",
        "Saidies",
        # More variations
        "Sadee's",
        "Sadey's",
        "Saidy's",
        "Saydie's",
        "Saedie's",
        "Saidey's",
        "Saedy's",
        "Saedie's",
        "Saidie's",
        "Saedee's",
        "Saidee's",
        "Sadei's",
        "Saide's",
        "Sadies'",
        "Sadies",
        # Changed capitalization
        "sadie's",
        "SADIE'S",
        "Sadies",
    ]

    for variation in variations:
        hash_value = hash_word(variation)
        if hash_value == target_hash:
            return variation

    return None

# Process each mismatched word
results = []

for idx, word, target_hash in mismatches:
    print(f"\n\nProcessing {idx}: '{word}' (target hash: {target_hash})")
    found = False

    # Check exact match first (just to verify our mismatches are correct)
    current_hash = hash_word(word)
    if current_hash == target_hash:
        results.append((idx, word, word, "exact match"))
        found = True
        continue

    # Try apostrophe variations first (for possessives like Sadie's, Watson's)
    if "'" in word:
        print(f"  Trying apostrophe variations for '{word}'...")
        result = try_apostrophe_variations(word, target_hash)
        if result:
            print(f"  MATCH FOUND: '{result}' (apostrophe variation)")
            results.append((idx, word, result, "apostrophe variation"))
            found = True
            continue

    # Special case for "Sadie's"
    if word == "Sadie's":
        print(f"  Trying special variations for '{word}'...")
        result = try_sadie_variations(target_hash)
        if result:
            print(f"  MATCH FOUND: '{result}' (special variation)")
            results.append((idx, word, result, "special variation"))
            found = True
            continue

    # Try character substitutions
    print(f"  Trying character substitutions for '{word}'...")
    result = try_char_substitutions(word, target_hash)
    if result:
        print(f"  MATCH FOUND: '{result}' (substitution)")
        results.append((idx, word, result, "substitution"))
        found = True
        continue

    # Try character deletions
    print(f"  Trying character deletions for '{word}'...")
    result = try_char_deletions(word, target_hash)
    if result:
        print(f"  MATCH FOUND: '{result}' (deletion)")
        results.append((idx, word, result, "deletion"))
        found = True
        continue

    # Try character insertions
    print(f"  Trying character insertions for '{word}'...")
    result = try_char_insertions(word, target_hash)
    if result:
        print(f"  MATCH FOUND: '{result}' (insertion)")
        results.append((idx, word, result, "insertion"))
        found = True
        continue

    # Try character swaps
    print(f"  Trying character swaps for '{word}'...")
    result = try_char_swaps(word, target_hash)
    if result:
        print(f"  MATCH FOUND: '{result}' (swap)")
        results.append((idx, word, result, "swap"))
        found = True
        continue

    # Try case variations
    print(f"  Trying case variations for '{word}'...")
    result = try_case_variations(word, target_hash)
    if result and result != word:
        print(f"  MATCH FOUND: '{result}' (case variation)")
        results.append((idx, word, result, "case variation"))
        found = True
        continue

    if not found:
        print(f"  NO MATCH FOUND for '{word}'")

# Print final results
print("\n\n===== RESULTS =====")
if results:
    for idx, original, corrected, method in results:
        print(f"Index {idx}: '{original}' -> '{corrected}' ({method})")
else:
    print("No matches found for any of the mismatched words.")