import hashlib
import string
import itertools

# The known 9-digit key
key = "485066843"
key_bytes = key.encode("utf-8")

# Word and target hash
word = "waiting"
target_hash = "9291c4d7338648be9c05d86fdb4124f9"

print(f"Searching for variations of '{word}' that match hash: {target_hash}\n")

def hash_word(test_word):
    return hashlib.md5(key_bytes + test_word.encode("utf-8")).hexdigest()

# Check the original word
original_hash = hash_word(word)
print(f"Original word '{word}' produces hash: {original_hash}")
print(f"Target hash: {target_hash}")
print(f"Match: {original_hash == target_hash}\n")

# Simple variations with capitalization
variations = [
    word.upper(),
    word.capitalize(),
    word.title(),
]

print("Checking common spelling variations...")

# Common misspellings
misspellings = [
    "waitin",    # drop g
    "waitng",    # drop i
    "wating",    # drop i
    "waitting",  # double t
    "waiiting",  # double i
    "waiteing",  # add e
    "waitnig",   # swap n and i
    "waitihg",   # replace n with h
    "wating",    # remove i
    "waighting", # add h
    "wating",    # drop ai -> a
    "wateing",   # drop ai -> ae
    "weiting",   # replace ai with ei
    "wayting",   # replace ai with ay
    "waitiing",  # double i
    "waittin",   # double t, drop g
    "wiaiting",  # swap a and i
    "wating",    # drop i
    "waitin'",   # apostrophe instead of g
    "waiten",    # replace ing with en
    "waeiting",  # insert e
    "wahaiting", # insert h
    "waiating",  # insert a
    "waitinga",  # append a
    "awaitin",   # prepend a, drop g
    "waitin",    # drop g
    "waiti",     # drop ng
    "waiting'",  # add apostrophe
    "wait'ing",  # add apostrophe in the middle
    "waitning",  # add n
    "waitingn",  # add n at the end
    "wwaiting",  # double w
    "waithing",  # replace i with h
    "waitinng",  # double n
    "wating",    # remove the i
    "aiting",    # remove the w
    "whating",   # replace waiting with whating
    "witing",    # remove the a
    "waining",   # replace t with n
    "waihing",   # replace t with h
    "waiding",   # replace t with d
    "wairing",   # replace t with r
    "Waiting",   # capitalize
    "waiiing",   # replace t with i
]

# Add all variations to the list
variations.extend(misspellings)

# Try all one-character substitutions
print("Trying all one-character substitutions...")
for i in range(len(word)):
    for char in string.ascii_lowercase:
        if char != word[i]:
            new_word = word[:i] + char + word[i+1:]
            variations.append(new_word)

# Try all one-character insertions
print("Trying all one-character insertions...")
for i in range(len(word) + 1):
    for char in string.ascii_lowercase:
        new_word = word[:i] + char + word[i:]
        variations.append(new_word)

# Try all one-character deletions
print("Trying all one-character deletions...")
for i in range(len(word)):
    new_word = word[:i] + word[i+1:]
    variations.append(new_word)

# Try all adjacent-character swaps
print("Trying all character swaps...")
for i in range(len(word) - 1):
    new_word = word[:i] + word[i+1] + word[i] + word[i+2:]
    variations.append(new_word)

# Try replacing "ing" with common variations
print("Trying ing-ending variations...")
if word.endswith("ing"):
    base = word[:-3]
    ing_variations = ["in", "ing'", "in'", "ign", "img", "inh", "ine", "ing ", " ing", "ings", "ing.", "ing,"]
    for v in ing_variations:
        variations.append(base + v)

# Try replacing "wait" with common typos
print("Trying wait-beginning variations...")
if word.startswith("wait"):
    endings = word[4:]
    wait_variations = ["wiat", "waht", "wat", "weit", "wiat", "wayt", "wiat", "wate", "waie", "whit", "woit", "writ"]
    for v in wait_variations:
        variations.append(v + endings)

# Make sure each variation is unique
unique_variations = list(set(variations))
print(f"\nTrying {len(unique_variations)} unique variations...\n")

# Try all variations
found = False
for variation in unique_variations:
    current_hash = hash_word(variation)
    if current_hash == target_hash:
        print(f"MATCH FOUND! '{variation}' produces the target hash!")
        print(f"  Original word: '{word}'")
        print(f"  Matched word:  '{variation}'")
        found = True
        break

if not found:
    print(f"No variation of '{word}' found that matches the target hash.")

# If we didn't find a match, try some two-character variations
if not found:
    print("\nTrying two-character substitutions (this might take a while)...")

    # Try substituting two characters (edit distance of 2)
    for i, j in itertools.combinations(range(len(word)), 2):
        for char1 in string.ascii_lowercase:
            for char2 in string.ascii_lowercase:
                if char1 != word[i] and char2 != word[j]:
                    chars = list(word)
                    chars[i] = char1
                    chars[j] = char2
                    new_word = ''.join(chars)
                    current_hash = hash_word(new_word)
                    if current_hash == target_hash:
                        print(f"MATCH FOUND! '{new_word}' produces the target hash!")
                        print(f"  Original word: '{word}'")
                        print(f"  Matched word:  '{new_word}'")
                        found = True
                        break
            if found:
                break
        if found:
            break