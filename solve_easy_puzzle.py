import hashlib
import string
from collections import defaultdict

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

# Try to build a custom word list
print(f"Attempting to decode hashes with key: {key}")

# First, try common English words from a comprehensive list
with open("wordlist.txt", "w") as f:
    # Write a comprehensive list of English words to try
    word_list = [
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

        # Additional useful words
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
        'hand', 'arm', 'leg', 'foot', 'feet', 'paris', 'london', 'berlin', 'madrid',
        'rome', 'vienna', 'moscow', 'tokyo', 'beijing', 'hong', 'kong', 'york', 'angeles',
        'francisco', 'washington', 'chicago', 'boston', 'seattle', 'miami', 'francisco',
        'austin', 'houston', 'atlanta', 'dallas', 'denver', 'phoenix', 'portland',

        # Words from the partially decoded message
        'agent', 'fly', 'from', 'to', 'the', 'other', 'side', 'of', 'at', 'three',
        'days', 'before', 'the', 'event', 'was', 'to', 'take', 'place', 'he',
        'a', 'note', 'on', 'the', 'door', 'of', 'his', 'little', 'yellow',
        'on', 'the', 'of', 'I', 'will', 'take', 'off', 'from',
        'and', 'fly', 'away', 'on', 'my', 'own', 'forgive', 'I', 'you', 'agent'
    ]

    # Add more words specifically for the context we've discovered
    # Context-specific words
    context_words = [
        'america', 'airplane', 'airport', 'flight', 'france', 'germany', 'england', 'russia',
        'plane', 'helicopter', 'hangar', 'barn', 'cottage', 'cabin', 'home', 'house',
        'london', 'paris', 'berlin', 'moscow', 'washington', 'york', 'chicago',
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
        'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december', 'secret', 'mission', 'cover',
        'wrote', 'written', 'signed', 'posted', 'attached', 'affixed', 'pinned', 'taped',
        'morning', 'afternoon', 'evening', 'night', 'midnight', 'noon', 'oclock', 'pm', 'am',
        'aircraft', 'pilot', 'spy', 'operation', 'mission', 'CIA', 'FBI', 'MI6', 'KGB',
        'special', 'classified', 'top', 'secret', 'password', 'code', 'cipher', 'encrypted',
        'government', 'military', 'intelligence', 'counter', 'espionage', 'undercover',
        'loved', 'miss', 'goodbye', 'farewell', 'adieu', 'godspeed', 'please', 'sorry'
    ]

    # Write all words to the file
    for word in set(word_list + context_words):
        f.write(word + "\n")

    # Add common name patterns
    for name in ['john', 'robert', 'james', 'william', 'david', 'richard', 'joseph', 'thomas',
                'charles', 'mary', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara',
                'susan', 'jessica', 'sarah', 'smith', 'johnson', 'williams', 'jones', 'brown',
                'davis', 'miller', 'wilson', 'moore', 'taylor', 'anderson', 'thomas', 'jackson']:
        f.write(name + "\n")
        f.write(name.title() + "\n")  # Capitalized version

    # Add common locations
    for location in ['new york', 'los angeles', 'chicago', 'san francisco', 'washington dc',
                    'london', 'paris', 'berlin', 'moscow', 'tokyo', 'beijing', 'hong kong']:
        f.write(location + "\n")
        f.write(location.replace(" ", "") + "\n")  # No spaces

    # Add numbers
    for num in range(100):
        f.write(str(num) + "\n")

# Now check each word in our wordlist
print("Trying words from our custom wordlist...")
with open("wordlist.txt", "r") as f:
    for word in f:
        word = word.strip().lower()
        if word:
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
    print("Dictionary file not found.")

# Reconstruct the message
message = []
for i in range(len(hashes)):
    if i in decoded_words:
        message.append(decoded_words[i])
    else:
        message.append("[UNKNOWN:" + hashes[i] + "]")

print("\nDecoded message:")
print(" ".join(message))

# Print stats
decoded_count = sum(1 for word in message if not word.startswith("[UNKNOWN"))
print(f"\nDecoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)")

# Display hashes we couldn't decode
if decoded_count < len(hashes):
    print("\nRemaining unknown hashes:")
    unknown_indexes = [i for i in range(len(hashes)) if i not in decoded_words]
    for idx in unknown_indexes:
        print(f"{idx}: {hashes[idx]}")

# Dump results to file for further analysis
print("Writing results to decoded_message.txt...")
with open("decoded_message.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Remaining unknown hashes:\n")
    for idx in range(len(hashes)):
        if idx not in decoded_words:
            f.write(f"{idx}: {hashes[idx]}\n")