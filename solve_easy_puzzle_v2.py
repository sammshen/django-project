import hashlib

# Read the puzzle file
with open("puzzle/PUZZLE-EASY", "r") as f:
    hashes = [line.strip() for line in f.readlines()]

# We know the key is 6346 from our previous run
key = "6346"
decoded_words = {}

# Make a dict of hash -> index for easy lookup
hash_to_index = {hash_val: idx for idx, hash_val in enumerate(hashes)}

# Function to check if a word matches any of our hashes
def check_word(word):
    word_hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
    if word_hash in hash_to_index:
        idx = hash_to_index[word_hash]
        decoded_words[idx] = word
        return True
    return False

print(f"Attempting to decode hashes with key: {key}")

# Try a large set of common words
common_words = [
    # Most common English words
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people',
    'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than',
    'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back',
    'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
    'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',

    # Additional useful words based on partial decoding
    'agent', 'spy', 'secret', 'mission', 'fly', 'door', 'yellow', 'side', 'note',
    'little', 'days', 'before', 'event', 'place', 'forgive', 'away', 'own',
    'airplane', 'flight', 'plane', 'morning', 'afternoon', 'evening', 'night',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
    'september', 'october', 'november', 'december', 'secret', 'message',
    'house', 'building', 'car', 'boat', 'ship', 'train', 'helicopter', 'jet',
    'city', 'town', 'country', 'street', 'road', 'avenue', 'boulevard', 'lane',
    'east', 'west', 'north', 'south', 'left', 'right', 'top', 'bottom', 'center',
    'am', 'pm', 'midnight', 'noon', 'dawn', 'dusk', 'sunrise', 'sunset',
    'today', 'tomorrow', 'yesterday', 'week', 'month', 'year', 'century', 'decade',
    'second', 'minute', 'hour', 'was', 'were', 'been', 'being', 'am', 'is', 'are',
    'had', 'has', 'having', 'do', 'does', 'did', 'doing', 'going', 'gone', 'went',
    'love', 'hate', 'hope', 'wish', 'want', 'need', 'must', 'should', 'shall', 'will',
    'would', 'could', 'might', 'may', 'can', 'tell', 'said', 'says', 'talk', 'speak',
    'listen', 'hear', 'watch', 'see', 'look', 'observe', 'notice', 'find', 'found',
    'search', 'seek', 'sought', 'come', 'came', 'coming', 'bring', 'brought', 'take',
    'took', 'taken', 'paper', 'letter', 'email', 'phone', 'call', 'text', 'message',
    'write', 'wrote', 'written', 'read', 'reading', 'begin', 'began', 'begun', 'start',
    'end', 'finish', 'complete', 'stop', 'close', 'open', 'shut', 'leave', 'left',
    'return', 'returned', 'head', 'face', 'eyes', 'nose', 'mouth', 'ears', 'hair',
    'hand', 'arm', 'leg', 'foot', 'feet',

    # Cities and countries
    'paris', 'london', 'berlin', 'madrid', 'moscow', 'tokyo', 'beijing', 'york',
    'chicago', 'boston', 'seattle', 'miami', 'austin', 'houston', 'atlanta', 'dallas',
    'america', 'france', 'germany', 'england', 'russia', 'china', 'japan', 'india',

    # Specific to the decoded message context
    'cottage', 'cabin', 'home', 'wrote', 'written', 'signed', 'posted', 'attached',
    'aircraft', 'pilot', 'operation', 'CIA', 'FBI', 'classified', 'government',
    'military', 'intelligence', 'counter', 'espionage', 'undercover', 'loved',
    'miss', 'goodbye', 'farewell', 'please', 'sorry',
    'station', 'airport', 'desk', 'safe', 'knew', 'told', 'sending', 'commander',
    'office', 'bureau', 'program', 'assignment', 'duty', 'task', 'job',
    'warning', 'escape', 'defect', 'defected', 'defection', 'caught', 'captured',
    'pursued', 'chased', 'apprehended', 'detected', 'discovered', 'exposed'
]

# Try common words
print("Trying common words...")
for word in common_words:
    check_word(word)

# Try a dictionary file if available
try:
    print("Trying words from dictionary file...")
    with open('/usr/share/dict/words', 'r') as dictionary:
        for word in dictionary:
            word = word.strip().lower()
            if 2 <= len(word) <= 15:  # Reasonable word length
                check_word(word)
except FileNotFoundError:
    print("Dictionary file not found, using a more limited set of words.")

# Reconstruct the message
message = []
for i in range(len(hashes)):
    if i in decoded_words:
        message.append(decoded_words[i])
    else:
        message.append(f"[UNKNOWN-{i}]")

print("\nDecoded message:")
print(" ".join(message))

# Print stats
decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

# Display hashes we couldn't decode
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
    for idx in unknown_indexes:
        f.write(f"{idx}: {hashes[idx]}\n")