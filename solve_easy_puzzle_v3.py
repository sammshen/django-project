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
    "agent", "fly", "from", "to", "the", "other", "side", "of", "at", "three",
    "days", "before", "event", "was", "take", "place", "he", "a", "note", "on",
    "door", "his", "little", "yellow", "will", "take", "off", "from", "and",
    "fly", "away", "on", "my", "own", "forgive", "I", "loved", "you", "agent"
]

# More domain-specific word lists
aviation_terms = [
    "cockpit", "pilot", "passenger", "runway", "airport", "landing", "takeoff",
    "altitude", "airspace", "navigation", "coordinates", "compass", "controls",
    "airframe", "fuselage", "wings", "propeller", "turbine", "instrument", "panel",
    "radar", "radio", "communication", "tower", "beacon", "beacon", "transponder"
]

spy_terms = [
    "spy", "espionage", "intelligence", "operation", "handler", "asset", "informant",
    "cover", "mission", "headquarters", "encrypted", "cipher", "code", "classified",
    "secret", "confidential", "covert", "surveillance", "embassy", "diplomat",
    "recruit", "defect", "defector", "enemy", "ally", "extraction", "safe", "house"
]

communication_terms = [
    "said", "wrote", "told", "informed", "advised", "instructed", "ordered",
    "communicated", "signaled", "messaged", "called", "emailed", "letter",
    "message", "report", "document", "dossier", "file", "folder", "briefing",
    "debriefing", "meeting", "rendezvous", "contact"
]

emotions = [
    "happy", "sad", "angry", "afraid", "worried", "concerned", "excited", "nervous",
    "anxious", "calm", "peaceful", "frustrated", "disappointed", "relieved", "sorry",
    "regretful", "guilty", "proud", "ashamed", "grateful", "thankful", "hopeful"
]

times = [
    "morning", "afternoon", "evening", "night", "dawn", "dusk", "noon", "midnight",
    "today", "tomorrow", "yesterday", "week", "month", "year", "hour", "minute",
    "second", "moment", "instant", "day", "night", "weekend", "weekday", "fortnight"
]

places = [
    "house", "home", "office", "building", "headquarters", "base", "station", "outpost",
    "room", "apartment", "flat", "penthouse", "cottage", "cabin", "villa", "mansion",
    "shack", "hut", "shelter", "hangar", "shed", "garage", "barn", "field", "forest",
    "mountain", "river", "lake", "ocean", "sea", "beach", "desert", "jungle", "town",
    "city", "village", "suburb", "neighborhood", "district", "region", "country",
    "continent", "island", "peninsula", "cape", "bay", "gulf", "strait", "channel", "london",
    "paris", "berlin", "rome", "madrid", "moscow", "washington", "new york", "chicago",
    "los angeles", "san francisco", "tokyo", "beijing", "sydney", "cairo", "cape town"
]

# Try lots of words to decode the message
print(f"Attempting to decode hashes with key: {key}")

# Common English words (1000 most frequent)
common_words = []
try:
    print("Fetching common English words...")
    response = requests.get("https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt")
    if response.status_code == 200:
        common_words = response.text.splitlines()
        print(f"Fetched {len(common_words)} common words")
    else:
        print("Failed to fetch word list, using backup list")
except:
    print("Failed to fetch word list online, using backup list")

# Backup list of very common words
most_common_words = [
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
    'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
]

if not common_words:
    common_words = most_common_words

# Combine all word lists
all_words = (known_partial_message + common_words + aviation_terms + spy_terms +
             communication_terms + emotions + times + places)

# Deduplicate
all_words = list(set(all_words))

# Try each word
print(f"Trying {len(all_words)} words...")
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

# Try to guess the missing words by position
def guess_missing_words():
    # Common English bigrams, trigrams and phrasal patterns
    bigrams = [
        ('to', 'the'), ('in', 'the'), ('of', 'the'), ('on', 'the'), ('and', 'the'),
        ('for', 'the'), ('to', 'be'), ('at', 'the'), ('with', 'the'), ('from', 'the'),
        ('by', 'the'), ('I', 'am'), ('I', 'will'), ('I', 'have'), ('you', 'are'),
        ('he', 'was'), ('she', 'was'), ('will', 'be'), ('has', 'been'), ('have', 'been'),
        ('can', 'be'), ('going', 'to'), ('want', 'to'), ('need', 'to'), ('try', 'to'),
        ('has', 'to'), ('have', 'to'), ('would', 'be'), ('should', 'be'), ('could', 'be'),
        ('might', 'be'), ('will', 'have'), ('they', 'are'), ('is', 'a'), ('is', 'the'),
        ('as', 'a'), ('it', 'is'), ('this', 'is'), ('there', 'is'), ('that', 'is'),
        ('do', 'not'), ('does', 'not'), ('did', 'not'), ('is', 'not'), ('are', 'not'),
        ('was', 'not'), ('were', 'not'), ('has', 'not'), ('have', 'not'), ('had', 'not'),
        ('one', 'of'), ('some', 'of'), ('many', 'of'), ('most', 'of'), ('all', 'of'),
        ('none', 'of'), ('such', 'as'), ('rather', 'than'), ('more', 'than'), ('less', 'than'),
        ('other', 'than'), ('so', 'that'), ('such', 'that'), ('now', 'that'), ('given', 'that'),
        ('provided', 'that'), ('as', 'long'), ('as', 'much'), ('as', 'well'), ('as', 'if'),
        ('as', 'though'), ('even', 'if'), ('even', 'though'), ('so', 'as'), ('in', 'order'),
        ('in', 'case'), ('in', 'fact'), ('in', 'general'), ('in', 'particular'), ('in', 'addition'),
        ('in', 'conclusion'), ('for', 'example'), ('for', 'instance'), ('such', 'as'),
        ('due', 'to'), ('according', 'to'), ('regardless', 'of'), ('with', 'regard')
    ]

    # Phrases specific to our partial decoded message
    spy_phrases = [
        ('secret', 'agent'), ('fly', 'away'), ('take', 'off'), ('the', 'door'),
        ('little', 'yellow'), ('loved', 'you'), ('please', 'forgive'), ('spy', 'agency'),
        ('other', 'side'), ('the', 'event'), ('on', 'my'), ('my', 'own'), ('and', 'fly')
    ]

    # Check for adjacent bigrams
    message_list = [decoded_words.get(i, None) for i in range(len(hashes))]

    # Try to fill in bigrams
    all_bigrams = bigrams + spy_phrases
    for bg in all_bigrams:
        for i in range(len(message_list) - 1):
            # If we have first word and missing second word
            if message_list[i] == bg[0] and message_list[i+1] is None:
                word = bg[1]
                if check_word(word):
                    message_list[i+1] = word

            # If we have second word and missing first word
            if message_list[i] is None and message_list[i+1] == bg[1]:
                word = bg[0]
                if check_word(word):
                    message_list[i] = word

# Try to guess some missing words
guess_missing_words()

# Try to decode using a list of known English words
def try_english_words():
    try:
        # Try downloading a larger list
        print("Trying a larger set of English words...")
        words_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        response = requests.get(words_url)
        if response.status_code == 200:
            words = response.text.splitlines()
            print(f"Downloaded {len(words)} English words")

            # Check only the words we haven't already decoded
            remaining_hashes = [hashes[i] for i in range(len(hashes)) if i not in decoded_words]
            remain_hash_set = set(remaining_hashes)
            print(f"Testing against {len(remain_hash_set)} remaining unique hashes")

            # Check in batches to show progress
            batch_size = 5000
            for i in range(0, len(words), batch_size):
                batch = words[i:i+batch_size]
                for word in batch:
                    word = word.strip().lower()
                    if 2 <= len(word) <= 15:  # Reasonable word length
                        check_word(word)

                print(f"Processed {min(i+batch_size, len(words))}/{len(words)} words, found {len(decoded_words)} total matches")

                # If we've decoded all words, stop early
                if len(decoded_words) == len(hashes):
                    break
    except Exception as e:
        print(f"Error trying English words: {e}")

# Try English words (commented out to avoid long runtime if not needed)
# try_english_words()

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

# Write results to file
with open("decoded_easy_message.txt", "w") as f:
    f.write(" ".join(message) + "\n\n")
    f.write(f"Decoded {decoded_count} out of {len(hashes)} words ({decoded_count/len(hashes)*100:.1f}%)\n\n")
    f.write("Key: " + key + "\n\n")
    f.write("Remaining unknown hashes:\n")
    for i in range(len(hashes)):
        if i not in decoded_words:
            f.write(f"{i}: {hashes[i]}\n")