import hashlib
import string
import requests
from collections import defaultdict

# Read the puzzle file
with open("puzzle/PUZZLE-EASY", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# We know the key is 6346 from our previous run
key = "6346"
decoded_words = {}

# Create a hash -> index mapping
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Try common English words
def check_word(word):
    word_hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
    if word_hash in hash_to_index:
        idx = hash_to_index[word_hash]
        if idx not in decoded_words:  # Don't overwrite existing decoded words
            decoded_words[idx] = word
            return True
    return False

# Words from the partially decoded message (from previous run)
known_partial_message = [
    "agent", "promised", "fly", "from", "to", "the", "other", "side", "of", "at", "three",
    "days", "before", "event", "was", "take", "place", "he", "a", "note", "on",
    "door", "his", "little", "yellow", "will", "take", "off", "from", "and",
    "fly", "away", "on", "my", "own", "forgive", "I", "loved", "you", "agent"
]

# Add more context-specific words
additional_words = [
    # Message text context
    "message", "secret", "mission", "agency", "letter", "warning", "escape", "plan",
    "leaving", "goodbye", "farewell", "adieu", "never", "again", "return", "home",
    "country", "government", "authorities", "police", "military", "intelligence",

    # Specific locations
    "moscow", "russia", "paris", "france", "berlin", "germany", "london", "england",
    "america", "states", "united", "washington", "york", "city", "chicago", "boston",

    # Time
    "oclock", "am", "pm", "morning", "afternoon", "evening", "night", "midnight",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "weekend", "tomorrow", "yesterday",

    # Buildings/structures
    "house", "apartment", "flat", "hotel", "motel", "cabin", "cottage", "hut",
    "mansion", "palace", "building", "structure", "office", "headquarters", "base",
    "station", "airport", "hangar", "runway", "garage",

    # Transportation
    "car", "vehicle", "automobile", "truck", "van", "motorcycle", "plane", "airplane",
    "aircraft", "jet", "helicopter", "boat", "ship", "yacht", "helicopter"
]

print(f"Attempting to decode hashes with key: {key}")

# Combine our word lists
all_words = known_partial_message + additional_words

# Try each word
print(f"Trying initial {len(all_words)} words...")
for word in all_words:
    word = word.strip().lower()
    if word:
        check_word(word)

# For hash values that appear multiple times, make sure they map to the same word
# Create a mapping from hash to word
hash_to_word = {}
for idx, word in decoded_words.items():
    hash_value = hashes[idx]
    hash_to_word[hash_value] = word

# Ensure consistency - apply the same word to all occurrences of a hash
for idx, hash_val in enumerate(hashes):
    if hash_val in hash_to_word and idx not in decoded_words:
        decoded_words[idx] = hash_to_word[hash_val]

# Add words that appear multiple times (the most common hashes)
print("\nChecking for repeated hashes...")
hash_counts = {}
for h in hashes:
    hash_counts[h] = hash_counts.get(h, 0) + 1

# Print the most common hashes that are still unknown
most_common_hashes = [(h, count) for h, count in hash_counts.items()
                     if count > 1 and h not in hash_to_word]
if most_common_hashes:
    print(f"Found {len(most_common_hashes)} hash values that appear multiple times:")
    for h, count in sorted(most_common_hashes, key=lambda x: x[1], reverse=True):
        print(f"  {h[:8]}... appears {count} times")

# Function to download the English words list and try each word
def try_english_words():
    try:
        # Try downloading a larger list
        print("\nTrying a larger set of English words...")
        words_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        response = requests.get(words_url)
        if response.status_code == 200:
            words = response.text.splitlines()
            print(f"Downloaded {len(words)} English words")

            # Check only the words we haven't already decoded
            remaining_hashes = set([hashes[i] for i in range(len(hashes)) if i not in decoded_words])
            print(f"Testing against {len(remaining_hashes)} remaining unique hashes")

            # Check in batches to show progress
            batch_size = 5000
            for i in range(0, len(words), batch_size):
                batch = words[i:i+batch_size]
                for word in batch:
                    word = word.strip().lower()
                    if 2 <= len(word) <= 15:  # Reasonable word length
                        check_word(word)

                # Print progress
                decoded_count = len(decoded_words)
                print(f"Processed {min(i+batch_size, len(words))}/{len(words)} words, found {decoded_count} total matches")

                # If we've decoded all words, stop early
                if len(decoded_words) == len(hashes):
                    break
    except Exception as e:
        print(f"Error trying English words: {e}")

# Comprehensive common word list as a fallback
def try_common_words():
    print("\nTrying comprehensive common word list...")
    common_word_url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"
    try:
        response = requests.get(common_word_url)
        if response.status_code == 200:
            words = response.text.splitlines()
            print(f"Got {len(words)} common words")
            for word in words:
                if word and 2 <= len(word) <= 15:
                    check_word(word)
    except Exception as e:
        print(f"Error fetching common words: {e}")

# Try the full dictionary
try_common_words()
try_english_words()

# Reconstruct the message
message = []
for i in range(len(hashes)):
    if i in decoded_words:
        message.append(decoded_words[i])
    else:
        message.append(f"[UNKNOWN-{i}:{hashes[i][:8]}]")

print("\nDecoded message:")
print(" ".join(message))

# Print stats
decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

# Display remaining unknown hashes
if decoded_count < len(hashes):
    print("\nRemaining unknown hash indexes:")
    unknown_indexes = [i for i in range(len(hashes)) if i not in decoded_words]
    for idx in unknown_indexes:
        print(f"{idx}: {hashes[idx]}")

# Write results to file
with open("decoded_easy_message.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Key: " + key + "\n\n")
    f.write("Remaining unknown hashes:\n")
    for i in range(len(hashes)):
        if i not in decoded_words:
            f.write(f"{i}: {hashes[i]}\n")