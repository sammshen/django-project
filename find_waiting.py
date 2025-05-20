import hashlib
import itertools
import string

# The known 9-digit key
key = "485066843"
key_bytes = key.encode("utf-8")

# Index and hash for the word "waiting" from our previous results
index = 73
original_hash = "9291c4d7338648be9c05d86fdb4124f9"
word = "waiting"

print(f"Trying to find the correct spelling for '{word}' at index {index}")
print(f"Target hash: {original_hash}")

# Function to check if a word matches the hash
def check_word(test_word):
    word_hash = hashlib.md5(key_bytes + test_word.encode("utf-8")).hexdigest()
    return word_hash == original_hash, word_hash

# 1. Try simple typos - swapping letters
print("\n1. Trying letter swaps...")
for i in range(len(word)-1):
    swapped = list(word)
    swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
    swapped_word = ''.join(swapped)
    matches, actual_hash = check_word(swapped_word)
    if matches:
        print(f"FOUND MATCH: '{swapped_word}'")
        exit(0)

# 2. Try adding a letter
print("\n2. Trying adding a letter...")
for i in range(len(word)+1):
    for char in string.ascii_lowercase:
        new_word = word[:i] + char + word[i:]
        matches, actual_hash = check_word(new_word)
        if matches:
            print(f"FOUND MATCH: '{new_word}'")
            exit(0)

# 3. Try removing a letter
print("\n3. Trying removing a letter...")
for i in range(len(word)):
    new_word = word[:i] + word[i+1:]
    matches, actual_hash = check_word(new_word)
    if matches:
        print(f"FOUND MATCH: '{new_word}'")
        exit(0)

# 4. Try substituting a letter
print("\n4. Trying substituting a letter...")
for i in range(len(word)):
    for char in string.ascii_lowercase:
        if char != word[i]:
            new_word = word[:i] + char + word[i+1:]
            matches, actual_hash = check_word(new_word)
            if matches:
                print(f"FOUND MATCH: '{new_word}'")
                exit(0)

# 5. Try capitalization variations
print("\n5. Trying capitalization variations...")
capitalization_variations = [
    word.lower(),
    word.upper(),
    word.capitalize(),
    ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word))
]
for variation in capitalization_variations:
    matches, actual_hash = check_word(variation)
    if matches:
        print(f"FOUND MATCH: '{variation}'")
        exit(0)

# 6. Try double letter variations
print("\n6. Trying double letter variations...")
for i in range(len(word)):
    new_word = word[:i] + word[i] + word[i:]
    matches, actual_hash = check_word(new_word)
    if matches:
        print(f"FOUND MATCH: '{new_word}'")
        exit(0)

# 7. Try common misspellings specifically for "waiting"
print("\n7. Trying common misspellings for 'waiting'...")
common_misspellings = [
    "wating",     # dropped i
    "waitting",   # doubled t
    "waeting",    # ae instead of ai
    "waiteing",   # added e
    "waitng",     # dropped i
    "waitting",   # doubled t
    "waitting",   # doubled tt
    "waitihg",    # h instead of n
    "waitign",    # transposed ng
    "waitin",     # dropped g
    "waiitng",    # doubled i, dropped i before n
    "waitiing",   # doubled i
    "wwaiting",   # doubled w
    "Waiting",    # capitalized
    "waeting",    # mixed spelling
    "wating",     # short form
    "waitin'",    # apostrophe
    "wating",     # single t
    "whating",    # added h after w
    "waiding",    # d instead of t
    "wating",     # missing i
    "wateing",    # missing i, added e
    "waitig",     # missing n
    "weiting",    # ei instead of ai
    "waightin",   # spelling variation
    "whaiting",   # added h
    "wayting",    # y instead of i
    "weyting",    # ey instead of ai
    "walting",    # l instead of i
    "widting",    # id instead of ai
]

for misspelling in common_misspellings:
    matches, actual_hash = check_word(misspelling)
    if matches:
        print(f"FOUND MATCH: '{misspelling}'")
        exit(0)

# If we reach here, we didn't find a match
print("\nNo match found for the given hash.")